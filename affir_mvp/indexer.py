import json
import os
import random
import string
from collections import defaultdict
from os.path import dirname, join
from typing import Dict, Optional, Set

from affir_mvp.token import Token


class Indexer:
    tokens_per_file: int = 30  # Сколько токенов хранится в одном JSON-файле
    index_folder = join(dirname(dirname(__file__)), "index")
    refs_file = os.path.join(index_folder, "refs.json")

    # Кеширование
    _refs_cache: Dict[str, str] = None
    _file_counts: Dict[str, int] = None
    _file_buffers: Dict[str, Dict[str, any]] = defaultdict(dict)

    @classmethod
    def _load_refs(cls) -> Dict[str, str]:
        """Кешируем refs в памяти"""
        if cls._refs_cache is None:
            if os.path.exists(cls.refs_file):
                with open(cls.refs_file, "r", encoding="utf-8") as f:
                    cls._refs_cache = json.load(f)
            else:
                cls._refs_cache = {}
        return cls._refs_cache

    @classmethod
    def _save_refs(cls):
        """Сохраняем refs только при изменениях"""
        with open(cls.refs_file, "w", encoding="utf-8") as f:
            json.dump(cls._refs_cache, f, ensure_ascii=False)

    @classmethod
    def _get_file_counts(cls) -> Dict[str, int]:
        """Кешируем количество токенов в файлах"""
        if cls._file_counts is None:
            cls._file_counts = defaultdict(int)
            for filename in set(cls._refs_cache.values()):
                filepath = os.path.join(cls.index_folder, filename)
                if os.path.exists(filepath):
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        cls._file_counts[filename] = len(data)
        return cls._file_counts

    @classmethod
    def _flush_buffer(cls, filename: str):
        """Сбрасываем буфер файла на диск"""
        if filename in cls._file_buffers:
            filepath = os.path.join(cls.index_folder, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(cls._file_buffers[filename], f, ensure_ascii=False)
            del cls._file_buffers[filename]

    @classmethod
    def _random_filename(cls) -> str:
        """Генерирует случайное имя файла длиной 10 символов."""
        return "".join(random.choices(string.ascii_letters, k=10)) + ".json"

    @classmethod
    def store_token(cls, token_data: Token, file_id: int):
        token = token_data.body
        refs = cls._load_refs()
        file_counts = cls._get_file_counts()

        # Для существующих токенов
        if token in refs:
            filename = refs[token]
            buffer = cls._file_buffers.get(filename)
            if not buffer:
                filepath = os.path.join(cls.index_folder, filename)
                if os.path.exists(filepath):
                    with open(filepath, "r", encoding="utf-8") as f:
                        buffer = json.load(f)
                else:
                    buffer = {}
                cls._file_buffers[filename] = buffer

            entry = buffer.setdefault(token, {})
            entries = entry.setdefault(str(file_id), [])
            entries.append((token_data.pos, token_data.index))
            # Сбрасываем на диск каждые 5000 изменений
            if len(cls._file_buffers[filename]) % 5000 == 0:
                cls._flush_buffer(filename)
        # Для новых токенов
        else:
            # Быстрый поиск файла с доступным местом
            filename = next(
                (f for f, cnt in file_counts.items() if cnt < cls.tokens_per_file), None
            )
            if not filename:
                filename = cls._random_filename()
                file_counts[filename] = 0
            # Обновляем кеши
            refs[token] = filename
            file_counts[filename] += 1
            # Добавляем в буфер
            buffer = cls._file_buffers[filename]
            buffer[token] = {str(file_id): [(token_data.pos, token_data.index)]}
            # Сбрасываем на диск при заполнении
            if file_counts[filename] >= cls.tokens_per_file:
                cls._flush_buffer(filename)
        # Периодическое сохранение refs
        if len(refs) % 5000 == 0:
            cls._save_refs()

    @classmethod
    def finalize(cls):
        """Сбрасываем все буферы и сохраняем refs"""
        for filename in list(cls._file_buffers.keys()):
            cls._flush_buffer(filename)
        cls._save_refs()
        cls._refs_cache = None
        cls._file_counts = None

    @classmethod
    def get_token_info(cls, token: str) -> Optional[Dict[str, Set[int]]]:
        """Возвращает информацию о токене, загружая соответствующий JSON-файл."""
        refs = cls._load_refs()
        if token not in refs:
            return None
        json_filepath = os.path.join(cls.index_folder, refs[token])
        if not os.path.exists(json_filepath):
            return None
        with open(json_filepath, "r", encoding="utf-8") as f:
            token_storage = json.load(f)
        return token_storage.get(token, {})

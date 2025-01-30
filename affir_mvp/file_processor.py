import json
import os
from os import listdir, path

from affir_mvp.indexer import Indexer
from affir_mvp.tokenizer import TokenizerPipeline


class FileProcessor:
    def __init__(self, data_folder: str, index_folder: str):
        """
        Класс для последовательной обработки файлов в указанной папке.
        :param index_path: Путь к папке с индексом.
        :param data_path: Путь к папке с файлами на обработку.
        """
        self.data_folder = data_folder
        self.index_folder = index_folder
        self.files_json = path.join(index_folder, "files.json")
        # Загружаем files.json (или создаем новый)
        self.file_map = self._load_files_json()
        self.next_id = int(max(self.file_map.keys(), default=0)) + 1  # Следующий доступный ID

    def _load_files_json(self) -> dict:
        """Загружает files.json или создает новый словарь, если файла нет."""
        if path.exists(self.files_json):
            with open(self.files_json, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_files_json(self):
        """Сохраняет актуальный files.json."""
        if not os.path.exists(self.index_folder):
            os.makedirs(self.index_folder)
        with open(self.files_json, "w", encoding="utf-8") as f:
            json.dump(self.file_map, f, ensure_ascii=False, indent=4)

    def process_files(self, tokenizer: TokenizerPipeline):
        """Обрабатывает каждый файл, назначает ID (если не назначен), и передает в токенизатор."""
        for root, _, files in os.walk(self.data_folder):  # Поддержка вложенных папок
            for file_name in sorted(files):  # Для стабильности сортируем файлы
                if not file_name.endswith(".txt"):
                    continue
                abs_file_path = path.join(root, file_name)
                rel_file_path = path.relpath(abs_file_path, self.data_folder)
                formatted_path = f"data/{rel_file_path}"  # Итоговый путь
                # Назначаем ID, если файла нет в files.json
                if formatted_path not in self.file_map.values():
                    self.file_map[str(self.next_id)] = formatted_path
                    self.next_id += 1
                    self._save_files_json()
                file_id = int(next(k for k, v in self.file_map.items() if v == formatted_path))
                # Читаем и передаем текст в токенизатор
                with open(abs_file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    tokenizer.run(content, file_id)

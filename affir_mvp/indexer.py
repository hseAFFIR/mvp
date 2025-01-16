import pickle
from typing import Dict, Optional, Set


class Indexer:
    # Хранилище токенов как атрибут класса
    _storage: Dict[str, Dict[int, Set[int]]] = {}

    @classmethod
    def store_token(cls, token: str, file_id: int, position: int, word_position: int) -> None:
        """
        Добавляет токен в индекс.

        :param token: Токен, который нужно сохранить.
        :param file_id: Идентификатор файла, в котором находится токен.
        :param position: Позиция токена в файле.
        """
        if token not in cls._storage:
            cls._storage[token] = {}
        if file_id not in cls._storage[token]:
            cls._storage[token][file_id] = set()
        cls._storage[token][file_id].add((position, word_position))

    @classmethod
    def get_token_info(cls, token: str) -> Optional[Dict[int, Set[int]]]:
        """
        Возвращает информацию о токене из индекса.

        :param token: Токен, который нужно найти.
        :return: Словарь с идентификаторами файлов и позициями токена или None,
        если токен отсутствует.
        """
        return cls._storage.get(token)

    @classmethod
    def save_storage(cls, filepath: str):
        try:
            with open(filepath, "wb") as file:
                pickle.dump(cls._storage, file)
            print(f"Структура успешно сохранена в файл: {filepath}")
        except Exception as e:
            print(f"Ошибка при сохранении структуры в файл: {e}")
            raise

    @classmethod
    def load_storage(cls, filepath: str):
        try:
            with open(filepath, "rb") as file:
                cls._storage = pickle.load(file)
            print(f"Структура успешно загружена из файла: {filepath}")
        except Exception as e:
            print(f"Ошибка при загрузке структуры из файла: {e}")
            raise

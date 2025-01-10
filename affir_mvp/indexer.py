from typing import Dict, Optional, Set


class Indexer:
    # Хранилище токенов как атрибут класса
    _storage: Dict[str, Dict[int, Set[int]]] = {}

    @classmethod
    def store_token(cls, token: str, file_id: int, position: int) -> None:
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
        cls._storage[token][file_id].add(position)

    @classmethod
    def get_token_info(cls, token: str) -> Optional[Dict[int, Set[int]]]:
        """
        Возвращает информацию о токене из индекса.

        :param token: Токен, который нужно найти.
        :return: Словарь с идентификаторами файлов и позициями токена или None,
        если токен отсутствует.
        """
        return cls._storage.get(token)

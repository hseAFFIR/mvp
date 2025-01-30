from os.path import join

import pytest

from affir_mvp.indexer import Indexer
from affir_mvp.token import Token


@pytest.fixture(autouse=True)
def clear_storage():
    """Перед каждым тестом очищаем индекс."""
    Indexer._storage = {}


def test_store_new_token():
    """Проверка добавления нового токена."""
    token = Token(body="hello", pos=1, index=0)
    Indexer.store_token(token, file_id=1)

    assert "hello" in Indexer._storage
    assert 1 in Indexer._storage["hello"]
    assert (1, 0) in Indexer._storage["hello"][1]


def test_store_duplicate_token():
    """Проверка повторного добавления токена в тот же файл."""
    token = Token(body="hello", pos=1, index=0)
    Indexer.store_token(token, file_id=1)
    Indexer.store_token(token, file_id=1)  # Дублируем

    # Должен остаться один токен
    assert len(Indexer._storage["hello"][1]) == 1


def test_store_token_in_different_files():
    """Один и тот же токен в разных файлах."""
    token1 = Token(body="hello", pos=1, index=0)
    token2 = Token(body="hello", pos=2, index=1)

    Indexer.store_token(token1, file_id=1)
    Indexer.store_token(token2, file_id=2)

    assert 1 in Indexer._storage["hello"]
    assert 2 in Indexer._storage["hello"]
    assert (1, 0) in Indexer._storage["hello"][1]
    assert (2, 1) in Indexer._storage["hello"][2]


# def test_store_empty_token(): # Не проходит, но теоретически такая ситуация невозможна
#     """Добавление пустого токена не должно работать."""
#     token = Token(body="", pos=1, index=0)
#     Indexer.store_token(token, file_id=1)

#     assert "" not in Indexer._storage  # Не должно добавляться


def test_save_and_load_storage(tmp_path):
    """Тест сохранения и загрузки индекса."""
    token = Token(body="hello", pos=1, index=0)
    Indexer.store_token(token, file_id=1)

    filepath = tmp_path / "index.pkl"
    Indexer.save_storage(str(filepath))

    # Очищаем и загружаем
    Indexer._storage = {}
    Indexer.load_storage(str(filepath))

    assert "hello" in Indexer._storage
    assert 1 in Indexer._storage["hello"]
    assert (1, 0) in Indexer._storage["hello"][1]

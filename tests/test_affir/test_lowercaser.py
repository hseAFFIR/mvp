import pytest

from affir_mvp.indexer import Indexer
from affir_mvp.tokenizer.filters import Htmler, Lowercaser
from affir_mvp.tokenizer.pipeline import TokenizerPipeline


@pytest.fixture(autouse=True)
def clear_storage():
    """Перед каждым тестом очищаем индекс."""
    Indexer._storage = {}


# Тест без фильтра на приведение к нижнему регистру
def test_tokenizer_without_lowercaser():
    tokenizer = TokenizerPipeline(Htmler())  # без Lowercaser
    word = "Hello World!"
    filtered_token = tokenizer.apply_filters(word)
    # Ожидаем, что токен останется без изменений
    assert filtered_token == word


# Тест с фильтром на приведение к нижнему регистру
def test_tokenizer_with_lowercaser():
    tokenizer = TokenizerPipeline(Lowercaser(), Htmler())  # с Lowercaser
    word = "Hello World!"
    filtered_token = tokenizer.apply_filters(word)
    # Ожидаем, что токен будет приведён к нижнему регистру
    assert filtered_token == "hello world!"

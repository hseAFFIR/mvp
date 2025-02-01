import pytest

from affir_mvp.indexer import Indexer
from affir_mvp.search import search
from affir_mvp.token import Token
from affir_mvp.tokenizer import TokenizerPipeline
from affir_mvp.tokenizer import filters as f


@pytest.fixture
def tokenizer():
    return TokenizerPipeline(
        f.Lowercaser(), f.Htmler(), f.Punctuator(), f.StopWords(), f.StemFilter()
    )


@pytest.fixture
def indexer():
    indexer = Indexer()
    Indexer._storage = {}

    # Добавление тестовых данных
    Indexer.store_token(Token("word1", 10, 0), 1)
    Indexer.store_token(Token("word2", 15, 1), 1)
    Indexer.store_token(Token("word3", 20, 2), 2)
    return indexer


def test_search(tokenizer, indexer):
    tokenizer.run = lambda text: [
        Token("word1", 0, 0),
        Token("word2", 0, 1),
    ]

    expected_result = {1: {10}}
    result = search("word1 word2", tokenizer)

    assert result == expected_result


def test_search_no_results(tokenizer, indexer):
    tokenizer.run = lambda text: [Token("unknown", 0, 0)]

    expected_result = {}
    result = search("unknown", tokenizer)

    assert result == expected_result


def test_search_multiple_files(tokenizer, indexer):
    tokenizer.run = lambda text: [Token("word3", 0, 0)]

    expected_result = {2: {20}}
    result = search("word3", tokenizer)

    assert result == expected_result


def test_search_partial_match(tokenizer, indexer):
    tokenizer.run = lambda text: [
        Token("word1", 0, 0),
        Token("wordX", 0, 1),
    ]

    expected_result = {}
    result = search("word1 wordX", tokenizer)

    assert result == expected_result


def test_search_with_real_index():
    Indexer.load_storage("storage.pkl")

    tokenizer = TokenizerPipeline()
    result = search("Бывало, выпустят два десятка снарядов", tokenizer)

    assert isinstance(result, dict)  # Проверка типа результата

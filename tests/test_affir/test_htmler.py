from os.path import dirname, join

import pytest

from affir_mvp.file_processor import FileProcessor
from affir_mvp.indexer import Indexer
from affir_mvp.search import search
from affir_mvp.tokenizer.filters import Htmler
from affir_mvp.tokenizer.pipeline import TokenizerPipeline


@pytest.fixture(autouse=True)
def clear_storage():
    """Перед каждым тестом очищаем индекс."""
    Indexer._storage = {}


# Тест без фильтра Htmler
def test_tokenizer_without_htmler():
    tokenizer = TokenizerPipeline()  # без Htmler
    word = "Hello World!"
    filtered_token = tokenizer.apply_filters(word)
    # Ожидаем, что токен останется без изменений
    assert filtered_token == word


@pytest.mark.parametrize(
    "word, expected_output",
    [
        ("<div>", None),  # строка с тегами и длиной меньше 10
        ("<", "<"),  # строка для тега длинной больше 10(обрезаеться в токинезаторе)
    ],
)
def test_tokenizer_with_htmler(word, expected_output):
    tokenizer = TokenizerPipeline(Htmler())  # с Htmler
    filtered_token = tokenizer.apply_filters(word)
    assert filtered_token == expected_output


@pytest.mark.parametrize(
    "word, expected_results",
    [
        (
            "HTML",
            {
                "file1.txt": {55},
                "file2.txt": {72, 122},
            },
        ),
        (
            "example",
            {
                "file2.txt": {109},
            },
        ),
        (
            "simple",
            {
                "file1.txt": {132},
            },
        ),
        (
            '<img src="path/folder/lib/png.zip">',
            {
                "file1.txt": {75},
            },
        ),
        (
            "<body>",
            {},
        ),
    ],
)
def test_search_with_htmler(word, expected_results):
    tokenizer = TokenizerPipeline(Htmler())

    root_path = dirname(dirname(__file__))
    folder_path = join(root_path, "tests_data/htmler")

    processor = FileProcessor(folder_path)
    processor.process_files(tokenizer)

    # Запуск поиска
    result = search(word, tokenizer)

    # Проверка, что для каждого слова мы получаем правильные файлы и позиции
    for file_key, expected_positions in expected_results.items():
        assert file_key in result  # Проверяем, что файл присутствует в результатах
        assert result[file_key] == expected_positions  # Проверяем, что позиции совпадают

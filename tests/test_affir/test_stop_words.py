from os.path import dirname, join

import pytest

from affir_mvp.tokenizer import TokenizerPipeline
from affir_mvp.tokenizer.filters import StopWords


def parse_stop_words(file_path):
    """Парсинг файла со стоп-словами: возвращает крайнее левое слово из строки."""
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            # Убираем комментарии и пустые строки
            if not line.strip() or "|" in line:
                continue
            # Берем крайнее левое слово
            word = line.split()[0]
            yield word


@pytest.mark.parametrize(
    "stop_word",
    list(
        parse_stop_words(
            join(dirname(dirname(__file__)), "tests_data", "stop_words", "stop_ru.txt")
        )
    )
    + list(
        parse_stop_words(
            join(dirname(dirname(__file__)), "tests_data", "stop_words", "stop_en.txt")
        )
    ),
)
def test_stop_words_filter(stop_word):
    """Тест фильтра стоп-слов."""
    tokenizer = TokenizerPipeline(StopWords())
    result = tokenizer.apply_filters(stop_word)
    assert result is None, f"Слово {stop_word} не отфильтровано"

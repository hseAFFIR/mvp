from os.path import dirname, join

import pytest

from affir_mvp.tokenizer import TokenizerPipeline
from affir_mvp.tokenizer.filters import StopWords


def parse_stop_words(file_path):
    """Парсинг файла со стоп-словами: возвращает крайнее левое слово из строки."""
    words = set()  # Используем множество для удаления дубликатов
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            # Убираем комментарии и пустые строки
            line = line.strip()
            if not line or line.startswith("|"):
                continue
            # Берем крайнее левое слово
            word = line.split()[0]
            words.add(word)
    return words


# Собираем уникальные слова из всех файлов
stop_words = list(
    parse_stop_words(join(dirname(dirname(__file__)), "tests_data", "stop_words", "stop_ru.txt"))
    | parse_stop_words(join(dirname(dirname(__file__)), "tests_data", "stop_words", "stop_en.txt"))
)


@pytest.mark.parametrize("stop_word", stop_words)
def test_stop_words_filter(stop_word):
    """Тест фильтра стоп-слов."""
    tokenizer = TokenizerPipeline(StopWords())
    result = tokenizer.apply_filters(stop_word)
    assert result is None, f"Слово {stop_word} не отфильтровано"

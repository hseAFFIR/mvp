# Путь к тестовым данным
import os

import pytest

from affir_mvp.tokenizer.filters.stemmer_eng import EnglishStemmer
from affir_mvp.tokenizer.filters.stemmer_ru import RussianPorterStemmer

root_path = os.path.dirname(os.path.dirname(__file__))
voc_ru_file = os.path.join(root_path, "tests_data", "stemmer", "voc_ru.txt")
output_ru_file = os.path.join(root_path, "tests_data", "stemmer", "output_ru.txt")
voc_en_file = os.path.join(root_path, "tests_data", "stemmer", "voc_en.txt")
output_en_file = os.path.join(root_path, "tests_data", "stemmer", "output_en.txt")


@pytest.mark.parametrize(
    "input_word, expected_stem",
    [
        (input_word.strip(), expected_stem.strip())
        for input_word, expected_stem in zip(
            open(voc_ru_file, encoding="utf-8").readlines(),
            open(output_ru_file, encoding="utf-8").readlines(),
        )
    ],
)
def test_russian_stemmer(input_word, expected_stem):
    # Создаем объект стеммера
    stem = RussianPorterStemmer()
    stemmed_word = stem.russian_stemmer(input_word)

    # Проверяем, что результат стеммера совпадает с ожидаемым
    assert stemmed_word == expected_stem, f"Expected {expected_stem}, got {stemmed_word}"


@pytest.mark.parametrize(
    "input_word, expected_stem",
    [
        (input_word.strip(), expected_stem.strip())
        for input_word, expected_stem in zip(
            open(voc_en_file, encoding="utf-8").readlines(),
            open(output_en_file, encoding="utf-8").readlines(),
        )
    ],
)
def test_english_stemmer(input_word, expected_stem):
    # Создаем объект стеммера
    stem = EnglishStemmer()
    stemmed_word = stem.english_stemmer(input_word)

    # Проверяем, что результат стеммера совпадает с ожидаемым
    assert stemmed_word == expected_stem, f"Expected |{expected_stem}|, got |{stemmed_word}|"

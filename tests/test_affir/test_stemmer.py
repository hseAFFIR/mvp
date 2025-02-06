import os

import pytest

from affir_mvp.tokenizer.filters.stemmer_eng import EnglishStemmer
from affir_mvp.tokenizer.filters.stemmer_ru import RussianPorterStemmer

root_path = os.path.dirname(os.path.dirname(__file__))
voc_ru_file = os.path.join(root_path, "tests_data", "stemmer", "voc_ru.txt")
output_ru_file = os.path.join(root_path, "tests_data", "stemmer", "output_ru.txt")
voc_en_file = os.path.join(root_path, "tests_data", "stemmer", "voc_en.txt")
output_en_file = os.path.join(root_path, "tests_data", "stemmer", "output_en.txt")


def load_stem_data(voc_file, output_file):
    """Функция для чтения данных из файлов."""
    with open(voc_file, encoding="utf-8") as voc_f, open(output_file, encoding="utf-8") as out_f:
        voc_lines = voc_f.readlines()
        output_lines = out_f.readlines()

    # Убираем лишние пробелы и передаем как кортежи
    return [(word.strip(), expected.strip()) for word, expected in zip(voc_lines, output_lines)]


def test_russian_stemmer():
    # Загружаем данные для русского стеммера
    test_data = load_stem_data(voc_ru_file, output_ru_file)

    stem = RussianPorterStemmer()

    for input_word, expected_stem in test_data:
        stemmed_word = stem.russian_stemmer(input_word)
        # Проверяем, что результат стеммера совпадает с ожидаемым
        assert stemmed_word == expected_stem, f"Expected {expected_stem}, got {stemmed_word}"


def test_english_stemmer():
    # Загружаем данные для английского стеммера
    test_data = load_stem_data(voc_en_file, output_en_file)

    stem = EnglishStemmer()

    for input_word, expected_stem in test_data:
        stemmed_word = stem.english_stemmer(input_word)
        # Проверяем, что результат стеммера совпадает с ожидаемым
        assert stemmed_word == expected_stem, f"Expected |{expected_stem}|, got |{stemmed_word}|"

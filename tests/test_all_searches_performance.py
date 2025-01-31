import time
from os.path import dirname, join

import pytest

import tester.searches as s
from affir_mvp.file_processor import FileProcessor
from affir_mvp.search import search
from affir_mvp.tokenizer import TokenizerPipeline

root_path = dirname(dirname(__file__))
folder_path = join(root_path, "data")

# Создаем экземпляр токенизатора и процессора
tokenizer = TokenizerPipeline()
processor = FileProcessor(folder_path)
processor.process_files(tokenizer)


@pytest.mark.parametrize(
    "word, expected_results",
    [
        (
            "поскакал к тому месту, откуда слышались выстрелы и где гуще был пороховой дым",
            {
                "Tolstoy_Lev_Voyna_i_mir_3-4.txt": {1091067},
            },
        ),
        (
            "-Владимир Константинович. Начинаем. Командуй кораблём.",
            {"admiral-_koronat_.txt": {63832}},
        ),
        (
            "6lib.ru - Электронная Библиотека",
            {
                "admiral-_koronat_.txt": {0},
                "ehe-raz-uviju_-ub_u_.txt": {0},
                "prisel_ci-i-sokroviha-piratov.txt": {0},
                "skol_naa-programma_-poezia-m_v_-lomonosova.txt": {0},
                "sobstvennaa-daha.txt": {0},
            },
        ),
        ("старшей дочери", {"Tolstoy_Lev_Voyna_i_mir_1-2.txt": {95826, 84836}}),
    ],
)
def test_all_searches_performance(word, expected_results):

    # Запуск поиска с использованием affir
    start_time = time.time()
    result_affir = search(word, tokenizer)
    end_time = time.time()
    elapsed_time_affir = (end_time - start_time) * 1000  # в миллисекундах
    print(f"affir search time - {elapsed_time_affir:.2f} ms")

    # Запуск поиска с использованием findall
    start_time = time.time()
    result_findall = s.search_with_findall(word.split("  "), folder_path)
    end_time = time.time()
    elapsed_time_findall = (end_time - start_time) * 1000
    print(f"findall search time - {elapsed_time_findall:.2f} ms")

    # Запуск поиска с использованием for
    start_time = time.time()
    result_for = s.search_with_for(word.split("  "), folder_path)
    end_time = time.time()
    elapsed_time_for = (end_time - start_time) * 1000
    print(f"for search time - {elapsed_time_for:.2f} ms")

    # Запуск поиска с использованием find
    start_time = time.time()
    result_find = s.search_with_find(word.split("  "), folder_path)
    end_time = time.time()
    elapsed_time_find = (end_time - start_time) * 1000
    print(f"find search time - {elapsed_time_find:.2f} ms\n\n")

    # Определяем минимальное время среди всех поисков
    min_time = min(elapsed_time_findall, elapsed_time_find, elapsed_time_for)

    # Проверка результатов для каждого поиска
    assert result_findall == expected_results, "результат findall неверный"
    assert result_for == expected_results, "результат for неверный"
    assert result_find == expected_results, "результат find неверный"
    assert result_affir == expected_results, "результат affir неверный"

    # Проверка времени для быстрого поиска
    assert (
        elapsed_time_affir < min_time
    ), f"Быстрый поиск занял слишком много времени: {elapsed_time_affir:.2f} миллисекунд"

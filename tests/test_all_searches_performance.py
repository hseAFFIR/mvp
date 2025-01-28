import time
from os.path import dirname, join

import pytest

from affir_mvp.file_processor import FileProcessor
from affir_mvp.search import search
from affir_mvp.tokenizer import TokenizerPipeline

# from findall_search import

root_path = dirname(dirname(__file__))
folder_path = join(root_path, "data")


def affir_search(word):
    tokenizer = TokenizerPipeline()

    processor = FileProcessor(folder_path)
    processor.process_files(tokenizer)

    # Запуск поиска
    start_time_affir = time.time()
    result = search(word, tokenizer)
    end_time_affir = time.time()

    elapsed_time_affir = (end_time_affir - start_time_affir) * 1000  # в миллисекундах

    return [result, elapsed_time_affir]


# def findall_search(word):


@pytest.mark.parametrize(
    "word, expected_results, max_time",
    [
        (
            "поскакал к тому месту, откуда слышались выстрелы и где гуще был пороховой дым",
            {
                "Tolstoy_Lev_Voyna_i_mir_3-4.txt": {1091067},
            },
            20,  # Максимальное время в миллисекундах
        ),
    ],
)
def test_4_searches(word, expected_results, max_time):

    result, elapsed_time_affir = affir_search(word)
    print(f"affir search time - {elapsed_time_affir:.2f} ms")

    assert result == expected_results
    assert (
        elapsed_time_affir < max_time
    ), f"Поиск занял слишком много времени: {elapsed_time_affir:.2f} миллисекунд"

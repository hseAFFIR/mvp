import time
from os.path import dirname, join

import pytest
from memory_profiler import memory_usage

from affir_mvp.file_processor import FileProcessor
from affir_mvp.tokenizer.filters import Htmler, Lowercaser, Punctuator, StemFilter
from affir_mvp.tokenizer.pipeline import TokenizerPipeline


@pytest.mark.parametrize(
    "filters, max_time, max_memory",
    [
        ([Lowercaser()], 5, 250),
        ([Htmler()], 7, 250),
        ([Punctuator()], 6, 250),
        ([StemFilter()], 8, 250),
        (
            [Lowercaser(), Htmler(), Punctuator(), StemFilter()],
            10,
            250,
        ),
    ],
)
def test_file_processing_time_and_memory(filters, max_time, max_memory):
    # Настройка путей
    root_path = dirname(dirname(__file__))
    # folder_path = join(root_path, "tests_data/big_dataset")
    folder_path = join(root_path, "..", "data")

    # Создание пайплайна с фильтрами
    tokenizer = TokenizerPipeline(*filters)

    # Создание процессора файлов
    processor = FileProcessor(folder_path)

    # Функция для выполнения замера памяти
    def process_files():
        processor.process_files(tokenizer)

    # Замер времени и памяти
    start_time = time.time()
    memory_before = memory_usage(max_usage=True)  # Замер до запуска
    process_files()
    memory_after = memory_usage(max_usage=True)  # Замер после выполнения
    end_time = time.time()

    # Расчёт затрат времени и памяти
    elapsed_time = end_time - start_time
    memory_used = memory_after - memory_before

    # Вывод результатов
    print(f"Время выполнения обработки: {elapsed_time:.2f} секунд")
    print(f"Использовано памяти: {memory_used:.2f} МБ")

    # Проверки
    assert (
        elapsed_time < max_time
    ), f"Обработка файлов заняла слишком много времени: {elapsed_time:.2f} секунд"
    assert (
        memory_used < max_memory
    ), f"Обработка файлов потребовала слишком много памяти: {memory_used:.2f} МБ"

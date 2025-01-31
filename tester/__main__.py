import time
from searches import search_with_for, search_with_findall, search_with_find

# Основная функция
if __name__ == "__main__":
    while True:
        folder_path = 'data'
        input_text = input("Введите слово или несколько слов: ")
        words = input_text.split('  ')  # Пробелы между словами считаются словосочетаниями

        # Запуск поиска с использованием разных методов
        start_time = time.time()
        result_for = search_with_for(words, folder_path)
        end_time = time.time()
        print("Результаты для цикла for:")
        print(result_for)
        print(f"Выполнено за {(end_time - start_time)*1000} мс\n")


        start_time = time.time()
        result_findall = search_with_findall(words, folder_path)
        end_time = time.time()
        print("Результаты для регулярных выражений (findall):")
        print(result_findall)
        print(f"Выполнено за {(end_time - start_time)*1000} мс\n")

        start_time = time.time()
        result_find = search_with_find(words, folder_path)
        end_time = time.time()
        print("Результаты для метода find:")
        print(result_find)
        print(f"Выполнено за {(end_time - start_time)*1000} мс\n")


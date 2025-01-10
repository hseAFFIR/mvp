import os
import time
import re

# Через findall

def count_word_in_folder(folder_path, target_word):
    total_time = 0
    total_count = 0
    
    # Создаем регулярное выражение для поиска целых слов
    word_pattern = re.compile(rf'\b{re.escape(target_word)}\b', re.IGNORECASE)  # Игнорируем регистр, если нужно

    # Проверяем, что папка существует
    if not os.path.exists(folder_path):
        print("Указанная папка не существует.")
        return

    # Перебираем все файлы в папке
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Проверяем расширение файла
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    # Считаем количество вхождений целых слов

                    start_time = time.time()
                    count = len(word_pattern.findall(content))
                    end_time = time.time()
                    total_time+=end_time - start_time

                   # print(f"В файле {filename} найдено {count} вхождений слова '{target_word}'.")
                    total_count += count
            except Exception as e:
                print(f"Не удалось обработать файл {filename}: {e}")

    
    print(f"\nОбщее количество вхождений слова '{target_word}': {total_count}")
    print(f"Время выполнения поиска: {total_time:.2f} секунд")

# Пример использования
folder_path = "data"  # Путь к папке
target_word = input("Введите слово для поиска:")  # Слово для поиска

count_word_in_folder(folder_path, target_word)

import os
import re
import time
from os.path import dirname, join


# finditer поиск
def count_word_in_folder(folder_path, target_word):
    total_count = 0
    word_positions = {}

    # Создаем регулярное выражение для поиска целых слов
    word_pattern = re.compile(
        rf"\b{re.escape(target_word)}\b", re.IGNORECASE
    )  # Игнорируем регистр, если нужно

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

                    # Считаем только вхождения токена, без записи позиций
                    matches = list(word_pattern.finditer(content))  # Найденные вхождения

                    if matches:
                        positions = {
                            match.start() for match in matches
                        }  # Индексы начала каждого совпадения
                        total_count += len(matches)
                        file_id = filename.split(".")[0]  # Можно использовать имя файла как id
                        word_positions[file_id] = positions

            except Exception as e:
                print(f"Не удалось обработать файл {filename}: {e}")

    return f"{word_positions}"


if __name__ == "__main__":
    root_path = dirname(dirname(__file__))
    folder_path = join(root_path, "data")

    while True:
        word = input("Введите слово: ")
        start_time = time.time()
        result = count_word_in_folder(folder_path, word)
        print(result)
        print(f"Выполнено за {(time.time() - start_time) * 1000} мс")

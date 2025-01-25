import os
import time
from os.path import dirname, join


# побуквенный поиск
def count_word_in_folder(folder_path, target_word):
    total_count = 0
    word_positions = {}

    target_word_lower = target_word.lower()

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
                    count = 0
                    positions = set()

                    # Перебираем символы текста вручную
                    word = ""
                    for index, char in enumerate(content):
                        if (
                            char.isalnum()
                        ):  # Если символ буква или цифра, добавляем в текущее слово
                            word += char.lower()
                        else:
                            if word == target_word_lower:  # Проверяем, совпадает ли слово
                                count += 1
                                positions.add(index - len(word))  # Добавляем позицию начала слова
                            word = ""  # Сбрасываем текущее слово

                    # Последнее слово (если текст не завершился разделителем)
                    if word == target_word_lower:
                        count += 1
                        positions.add(len(content) - len(word))  # Последняя позиция слова

                    total_count += count

                    if positions:  # Если были найдены позиции
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

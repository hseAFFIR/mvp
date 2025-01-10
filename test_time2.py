import os
import time

def count_word_in_folder(folder_path, target_word):
    total_count = 0
    total_time = 0
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
                    
                    # Время поиска слова
                    search_start_time = time.time()
                    count = 0
                    
                    # Перебираем символы текста вручную
                    word = ""
                    for char in content:
                        if char.isalnum():  # Если символ буква или цифра, добавляем в текущее слово
                            word += char.lower()
                        else:
                            if word == target_word_lower:  # Проверяем, совпадает ли слово
                                count += 1
                            word = ""  # Сбрасываем текущее слово
                    # Последнее слово (если текст не завершился разделителем)
                    if word == target_word_lower:
                        count += 1

                    search_end_time = time.time()
                    search_time = search_end_time - search_start_time
                    total_time+=search_time
                    
                    #print(f"В файле {filename} найдено {count} вхождений слова '{target_word}'.")
                    #print(f"Время поиска в файле {filename}: {search_time:.6f} секунд.")
                    total_count += count
            except Exception as e:
                print(f"Не удалось обработать файл {filename}: {e}")

    print(f"\nОбщее количество вхождений слова '{target_word}': {total_count}")
    print(f"Общее время поиска: {total_time:.6f} секунд.")
    

# Пример использования
folder_path = "data"  # Путь к папке
target_word = input("Введите слово для поиска:")  # Слово для поиска

count_word_in_folder(folder_path, target_word)

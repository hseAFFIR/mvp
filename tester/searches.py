import os
import re

# Поиск через цикл for
def search_with_for(words, folder_path):
    result = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                for phrase in words:
                    indices = {i for i in range(len(text)) if text[i:i+len(phrase)] == phrase and
                               (i == 0 or not text[i-1].isalnum()) and (i+len(phrase) == len(text) or not text[i+len(phrase)].isalnum())}
                    if indices:
                        result[f'{filename}:{text.count(phrase)}'] = indices
    return result

# Поиск через регулярные выражения (findall)
def search_with_findall(words, folder_path):
    result = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                for phrase in words:
                    # Регулярное выражение для точного совпадения фразы
                    indices = {m.start() for m in re.finditer(r'(?<!\w)' + re.escape(phrase) + r'(?!\w)', text)}
                    if indices:
                        result[f'{filename}:{text.count(phrase)}'] = indices
    return result

# Поиск через метод find
def search_with_find(words, folder_path):
    result = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                for phrase in words:
                    start = 0
                    indices = set()
                    while True:
                        start = text.find(phrase, start)
                        if start == -1:
                            break
                        # Проверяем, что перед и после фразы нет других символов
                        if (start == 0 or not text[start-1].isalnum()) and (start+len(phrase) == len(text) or not text[start+len(phrase)].isalnum()):
                            indices.add(start)
                        start += len(phrase)
                    if indices:
                        result[f'{filename}:{text.count(phrase)}'] = indices
    return result

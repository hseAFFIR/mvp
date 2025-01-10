import pickle

global TOKEN_STORAGE

TOKEN_STORAGE = dict()

def store_token(token: str, file_id: int, position: int):
    if token not in TOKEN_STORAGE:
        TOKEN_STORAGE[token] = {}
    if file_id in TOKEN_STORAGE[token]:
        TOKEN_STORAGE[token][file_id].add(position)
    else:
        TOKEN_STORAGE[token][file_id] = {position}

def get_token_info(token: str) -> dict | None:
    return TOKEN_STORAGE.get(token)

def save_token_storage_to_file(filepath: str):
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(TOKEN_STORAGE, file)
        print(f"Структура успешно сохранена в файл: {filepath}")
    except Exception as e:
        print(f"Ошибка при сохранении структуры в файл: {e}")

def load_token_storage_from_file(filepath: str):
    try:
        with open(filepath, 'rb') as file:
            TOKEN_STORAGE = pickle.load(file)
        print(f"Структура успешно загружена из файла: {filepath}")
    except Exception as e:
        print(f"Ошибка при загрузке структуры из файла: {e}")

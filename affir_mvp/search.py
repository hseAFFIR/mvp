from typing import Dict, List, Optional, Set

from affir_mvp.indexer import Indexer
from affir_mvp.tokenizer import TokenizerPipeline


def search(string_for_search: str, tokenizer: TokenizerPipeline) -> Optional[Dict[int, Set[int]]]:
    """
    Осуществляет поиск последовательности токенов в индексе.

    :param string_for_search: Строка для поиска.
    :param tokenizer: Экземпляр токенизатора, который возвращает список токенов с их длиной.
    :return: Словарь, где ключи — file_id, а значения — множества стартовых позиций (по п
    ервой букве токена),
             или пустой словарь, если совпадений нет.
    """

    # Токенизация строки для поиска
    tokens = tokenizer.run(string_for_search)

    if not tokens:
        return {}

    # Извлекаем токены
    token_sequence = [token.body for token in tokens]

    first_token = Indexer.get_token_info(token_sequence[0])
    if not first_token:
        return {}

    # Проверяем последовательность токенов в рамках каждого файла
    result = {}
    for file_id, positions in first_token.items():
        for start_position, start_word_pos in positions:  # Используем position и word_position
            # Проверяем, что все остальные токены идут подряд по word_position
            if all(
                Indexer.get_token_info(token_sequence[i])  # Токен существует в индексе
                and file_id in Indexer.get_token_info(token_sequence[i])  # Есть в этом файле
                and (start_word_pos + i)
                in {
                    pos[1] for pos in Indexer.get_token_info(token_sequence[i])[file_id]
                }  # Проверяем word_position
                for i in range(1, len(token_sequence))
            ):
                if file_id not in result:
                    result[file_id] = set()
                result[file_id].add(start_position)  # Добавляем position первой буквы

    return result

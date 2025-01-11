from typing import Dict, List, Optional, Set

from affir_mvp.indexer import Indexer
from affir_mvp.strategy import Strategy
from affir_mvp.tokenizer import TokenizerFactory

# def search(string_for_search: str) -> Optional[Dict[int, Set[int]]]:
#     """
#     Осуществляет поиск по индексу для указанного токена.

#     :param string_for_search: Строка для поиска.
#     :return: Результат поиска или None, если токен отсутствует.
#     """

#     tokenizer = TokenizerFactory.create_pipeline(Strategy.HIGH)

#     token_for_search = tokenizer.run(string_for_search)[0][0]  # пока ищем 1 слово

#     return Indexer.get_token_info(token_for_search)


def search(string_for_search: str, tokenizer) -> Optional[Dict[int, Set[int]]]:
    """
    Осуществляет поиск последовательности токенов в индексе.

    :param string_for_search: Строка для поиска.
    :return: Словарь, где ключи — file_id, а значения — множества стартовых позиций,
             или пустой словарь, если совпадений нет.
    """

    # Токенизация строки для поиска
    tokens_with_positions = tokenizer.run(string_for_search)  # list[tuple[str, int]]

    if not tokens_with_positions:
        return {}

    # Извлекаем токены и их длины
    token_sequence = [(token, len(token)) for token, _ in tokens_with_positions]

    # Получаем позиции первого токена
    first_token, _ = token_sequence[0]
    first_token_positions = Indexer.get_token_info(first_token)
    if not first_token_positions:
        return {}

    # Проверяем последовательность токенов в рамках каждого файла
    result = {}
    for file_id, positions in first_token_positions.items():
        for start_pos in positions:
            # Проверяем, что все остальные токены идут подряд
            if all(
                Indexer.get_token_info(token_sequence[i][0])  # Токен существует в индексе
                and file_id in Indexer.get_token_info(token_sequence[i][0])  # Есть в этом файле
                and start_pos + sum(token_sequence[j][1] + 1 for j in range(i))
                in Indexer.get_token_info(token_sequence[i][0])[file_id]  # Позиция совпадает
                for i in range(1, len(token_sequence))
            ):
                if file_id not in result:
                    result[file_id] = set()
                result[file_id].add(start_pos)

    return result

from typing import Dict, Optional, Set

from affir_mvp.indexer import Indexer
from affir_mvp.modules.tokenizer_factory import TokenizerFactory
from affir_mvp.strategy import Strategy


def search(string_for_search: str) -> Optional[Dict[int, Set[int]]]:
    """
    Осуществляет поиск по индексу для указанного токена.

    :param string_for_search: Строка для поиска.
    :return: Результат поиска или None, если токен отсутствует.
    """

    factory = TokenizerFactory()
    tokenizer = factory.create_pipeline(Strategy.HIGH)

    tokens_for_search = tokenizer.run(string_for_search)[0]  # пока ищем 1 слово
    print(tokens_for_search)

    return Indexer.get_token_info(tokens_for_search[0])

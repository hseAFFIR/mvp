from typing import Dict, Optional, Set

from affir_mvp.indexer import Indexer
from affir_mvp.tokenizer import TokenizerPipeline
from affir_mvp.tokenizer.filters import Base


def search(string_for_search: str, *filters: Base) -> Optional[Dict[int, Set[int]]]:
    """
    Осуществляет поиск по индексу для указанного токена.

    :param string_for_search: Строка для поиска.
    :return: Результат поиска или None, если токен отсутствует.
    """

    tokenizer = TokenizerPipeline(*filters)

    token_for_search = tokenizer.run(string_for_search)[0].body  # пока ищем 1 слово

    return Indexer.get_token_info(token_for_search)

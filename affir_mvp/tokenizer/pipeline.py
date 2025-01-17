import re
from typing import Generator

from affir_mvp.indexer import Indexer
from affir_mvp.token import Token

from .filters.base import Base


class TokenizerPipeline:
    html_pattern = re.compile(r"<\/?\w+.*?>")
    MAX_HTML_LEN = 10

    def __init__(self):
        self.filters = []

    def run(self, text: str, file_id: str = None) -> list[Token]:
        res = []
        for token in self._tokenize(text):
            if file_id:
                Indexer.store_token(token, file_id)
            res.append(token)
        return res

    def _tokenize(self, text: str) -> Generator[Token, None, None]:
        current_position = 0
        index = 0

        while current_position < len(text):
            # Пропускаем пробелы
            if text[current_position].isspace():
                current_position += 1
                continue

            # Начинаем новый токен
            start_position = current_position
            token = ""

            # Возможно это html тег
            if text[start_position] == "<":
                res = self.html_pattern.match(
                    text, start_position, start_position + self.MAX_HTML_LEN
                )
                # Да, это html тег
                if res and res.start() == start_position:
                    token = res.group()
                    current_position = res.end()
                # Нет, это не html тег
                else:
                    token = text[start_position]
                    current_position += 1
            # Это другой символ
            elif not text[current_position].isalnum():
                token = text[start_position]
                current_position += 1
            # Это слово
            else:
                # Собираем символы токена
                while current_position < len(text) and text[current_position].isalnum():
                    token += text[current_position]
                    current_position += 1

            # Добавляем токен только если он не пустой
            token = self.apply_filters(token)
            if token:
                yield Token(token, start_position, index)
                index += 1

    def add_filter(self, filter: Base):
        self.filters.append(filter)

    def apply_filters(self, token: str) -> str | None:
        if not token:
            return None
        for filter in self.filters:
            filter: Base
            token = filter.process(token)
            if not token:
                break
        return token

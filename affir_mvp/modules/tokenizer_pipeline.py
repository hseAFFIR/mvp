from affir_mvp.indexer import Indexer

from .filters.base import Base


class TokenizerPipeline:
    def __init__(self):
        self.filters = []
        self.file_id = None

    def run(self, text: str) -> list[tuple[str, int]]:
        tokens = self._tokenize(text)
        return self.apply_filters(tokens)

    def set_file_id(self, file_id: str):
        self.file_id = file_id

    def _tokenize(self, text: str) -> list[tuple[str, int]]:
        tokens = []
        current_position = 0

        while current_position < len(text):
            # Пропускаем пробелы
            if text[current_position].isspace():
                current_position += 1
                continue

            # Начинаем новый токен
            start_position = current_position
            token = ""

            # Собираем символы токена
            while current_position < len(text) and not text[current_position].isspace():
                token += text[current_position]
                current_position += 1

            # Добавляем токен только если он не пустой
            if token:
                tokens.append((token, start_position))

        return tokens

    def add_filter(self, filter: Base):
        self.filters.append(filter)

    def apply_filters(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        for token, pos in tokens:
            for filter in self.filters:
                filter: Base
                token = filter.process(token)
            if self.file_id:
                Indexer.store_token(token=token, file_id=self.file_id, position=pos)
        return tokens

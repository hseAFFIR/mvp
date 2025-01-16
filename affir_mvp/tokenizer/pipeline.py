from affir_mvp.indexer import Indexer

from .filters.base import Base


class TokenizerPipeline:
    def __init__(self):
        self.filters = []
        self.file_id = None

    def run(self, text: str, file_id: str = None) -> list[tuple[str, int]]:
        if file_id:
            self.file_id = file_id
        tokens = self._tokenize(text)
        return self.apply_filters(tokens)

    def _tokenize(self, text: str) -> list[tuple[str, int]]:
        tokens = []
        current_position = 0
        word_possition = 0

        while current_position < len(text):
            # Пропускаем пробелы
            if text[current_position].isspace():
                current_position += 1
                word_possition += 1  # отслеживание позиции слова
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
                tokens.append((token, start_position, word_possition))

        return tokens

    def add_filter(self, filter: Base):
        self.filters.append(filter)

    def apply_filters(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        new_tokens = []
        for token, pos, word_pos in tokens:
            for filter in self.filters:
                filter: Base
                token = filter.process(token)
            new_tokens.append((token, pos))
            if self.file_id:
                Indexer.store_token(token, self.file_id, pos, word_pos)
        return new_tokens

from .filters.base import Base


class TokenizerPipeline:
    def __init__(self):
        self.filters = []

    def run(self, text: str) -> list[str]:
        tokens = self._tokenize(text)
        return self.apply_filters(tokens)

    def _tokenize(self, text: str) -> list[str]:
        return text.split()

    def add_filter(self, filter: Base):
        self.filters.append(filter)

    def apply_filters(self, tokens: list[str]) -> list[str]:
        for filter in self.filters:
            filter: Base
            tokens = filter.process(tokens)
        return tokens

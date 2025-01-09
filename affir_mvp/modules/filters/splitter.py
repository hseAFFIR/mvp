from .base import Base


class Splitter(Base):
    def process(self, tokens: list[str]) -> list[str]:
        res = []
        for token in tokens:
            res.extend(token.split())
        return res

from .base import Base


class Lowercaser(Base):
    def process(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        res = []
        for token, position in tokens:
            res.append((token.lower(), position))
        return res


from .base import Base


class Lowercaser(Base):

    def process(self, tokens: list[str]) -> list[str]:
        res = []
        for token in tokens:
            res.append(token.lower())
        return res

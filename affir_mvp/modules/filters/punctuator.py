from .base import Base

class Punctuator(Base):
    def process(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        res = []
        for token, position in tokens:
            new_token = "".join(ch for ch in token if ch.isalnum())
            res.append((new_token, position))  
        return res


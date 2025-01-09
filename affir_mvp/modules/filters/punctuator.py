from .base import Base


class Punctuator(Base):
    def process(self, tokens: list[str]) -> list[str]:
        res = []
        for token in tokens:
            new_token = ""
            for ch in token:
                if ch.isdigit() or ch.isalpha():
                    new_token += ch
            res.append(new_token)
        return res

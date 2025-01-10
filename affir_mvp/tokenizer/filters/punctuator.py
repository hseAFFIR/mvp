from .base import Base


class Punctuator(Base):
    def process(self, token: str) -> str:
        return "".join(ch for ch in token if ch.isalnum())

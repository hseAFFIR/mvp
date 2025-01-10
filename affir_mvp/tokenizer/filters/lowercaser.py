from .base import Base


class Lowercaser(Base):
    def process(self, token: str) -> str:
        return token.lower()

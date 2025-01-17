from .base import Base


class Punctuator(Base):
    def process(self, token: str) -> str:
        if len(token) == 1 and not token.isalnum():
            return None
        return token

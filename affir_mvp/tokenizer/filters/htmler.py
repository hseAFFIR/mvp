from .base import Base


class Htmler(Base):
    def process(self, token: str) -> str:
        if token[0] == "<" and len(token) > 1:
            return None
        return token

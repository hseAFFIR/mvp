from dataclasses import dataclass


@dataclass
class Token:
    body: str  # Слово
    pos: int  # Позция в тексте
    index: int  # Позиция среди токенов

from dataclasses import dataclass


@dataclass
class Token:
    body: str
    pos: int
    index: int

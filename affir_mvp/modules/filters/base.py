from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def process(self, tokens: list[str]) -> list[str]:
        pass

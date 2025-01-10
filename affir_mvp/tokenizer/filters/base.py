from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def process(self, token: str) -> str:
        pass

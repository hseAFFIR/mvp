from os.path import dirname, join

from .base import Base


class StopWords(Base):
    FOLDER_PATH = dirname(dirname(__file__))
    with open(join(FOLDER_PATH, "filters", "stop_words_ru.txt"), "r", encoding="utf-8") as file:
        STOP_WORDS_RU = set(word.strip() for word in file)
    with open(join(FOLDER_PATH, "filters", "stop_words_en.txt"), "r", encoding="utf-8") as file:
        STOP_WORDS_EN = set(word.strip() for word in file)

    def process(self, token: str) -> str:
        if token in self.STOP_WORDS_EN or token in self.STOP_WORDS_RU:
            return None
        return token

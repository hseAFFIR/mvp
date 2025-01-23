import re
from .base import Base
from .stemmer_eng import EnglishStemmer
from .stemmer_ru import RussianPorterStemmer

class StemFilter(Base):
    def __init__(self):
        self.english_stemmer = EnglishStemmer()  
        self.russian_stemmer = RussianPorterStemmer()  

    def detect_language(self, token):
        # Проверяем на наличие кириллицы
        if re.search(r'[а-яА-Я]', token):
            return 'ru'
        # Проверяем на наличие латиницы
        elif re.search(r'[a-zA-Z]', token):
            return 'en'
        else:
            return 'unknown'

    def process(self, token):
        try:
            lang = self.detect_language(token)  # Определяем язык токена
            if lang == 'ru':
                return self.russian_stemmer.russian_stemmer(token)  # Используем русский стеммер
            elif lang == 'en':
                return self.english_stemmer.english_stemmer(word=token)  # Используем английский стеммер
            else:
                return token  # Если язык не русский и не английский, возвращаем токен без изменений
        except Exception as e:
            # Обработка возможных ошибок, например, пустой токен или неизвестный язык
            print(f"Error detecting language or stemming: {e}")
            return token

    



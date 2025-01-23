import time
from os.path import dirname, join

from affir_mvp.file_processor import FileProcessor
from affir_mvp.indexer import Indexer
from affir_mvp.search import search
from affir_mvp.tokenizer import TokenizerPipeline
from affir_mvp.tokenizer import filters as f

if __name__ == "__main__":
    root_path = dirname(dirname(__file__))
    folder_path = join(root_path, "data")
    tokenizer = TokenizerPipeline(f.Lowercaser(), f.Htmler(), f.Punctuator(),f.StemFilter())
    try:
        Indexer.load_storage("storage.pkl")
    except Exception:
        print("Кеш отсутствует. Загружаем...")
        processor = FileProcessor(folder_path)
        processor.process_files(tokenizer)
        Indexer.save_storage("storage.pkl")

    while True:
        word = input("Введите слово: ")
        start_time = time.time()
        print(search(word, tokenizer))
        print(f"Выполнено за {(time.time() - start_time) * 1000} мс")
        # filtered_token = tokenizer.apply_filters(word)
        # print(f"Filtered token: {filtered_token}")

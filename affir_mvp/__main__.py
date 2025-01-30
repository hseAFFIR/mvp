import time
from os.path import dirname, join

from affir_mvp.file_processor import FileProcessor
from affir_mvp.indexer import Indexer
from affir_mvp.search import search
from affir_mvp.tokenizer import TokenizerPipeline
from affir_mvp.tokenizer import filters as f

if __name__ == "__main__":
    root_path = dirname(dirname(__file__))
    data_folder = join(root_path, "data")
    index_folder = join(root_path, "index")
    tokenizer = TokenizerPipeline(
        f.Lowercaser(), f.Htmler(), f.Punctuator(), f.StopWords(), f.StemFilter()
    )
    Indexer._load_refs()
    processor = FileProcessor(data_folder, index_folder)
    processor.process_files(tokenizer)  # Запускаем обработку файлов
    Indexer.finalize()
    while True:
        word = input("Введите слово: ")
        start_time = time.time()
        print(search(word, tokenizer))
        print(f"Выполнено за {(time.time() - start_time) * 1000} мс")

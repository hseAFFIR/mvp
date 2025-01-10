from os.path import dirname, join

from affir_mvp.file_processor import FileProcessor
from affir_mvp.search import search
from affir_mvp.strategy import Strategy
from affir_mvp.tokenizer import TokenizerFactory

if __name__ == "__main__":
    root_path = dirname(dirname(__file__))
    folder_path = join(root_path, "data")
    factory = TokenizerFactory()
    tokenizer = factory.create_pipeline(Strategy.HIGH)
    processor = FileProcessor(folder_path)
    processor.process_files(tokenizer)
    print(search("семья"))

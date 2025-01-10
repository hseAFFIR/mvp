import os

from affir_mvp.indexer import Indexer
from affir_mvp.modules.file_processor import FileProcessor
from affir_mvp.modules.tokenizer_factory import TokenizerFactory
from affir_mvp.search import search
from affir_mvp.strategy import Strategy

if __name__ == "__main__":
    root_path = os.path.dirname(os.path.dirname(__file__))
    folder_path = os.path.join(root_path, "data")
    factory = TokenizerFactory()
    tokenizer = factory.create_pipeline(Strategy.HIGH)
    processor = FileProcessor(folder_path, tokenizer)
    processor.process_files()
    # print(Indexer.get_token_info("семья"))
    print(search("семья"))

from os.path import dirname, join

import affir_mvp.indexer as indexer
from affir_mvp.modules.file_processor import FileProcessor
from affir_mvp.modules.tokenizer_factory import TokenizerFactory
from affir_mvp.strategy import Strategy

if __name__ == "__main__":
    folder_path = join(dirname(dirname(__file__)), "data")
    tokenizer = TokenizerFactory.create_pipeline(Strategy.HIGH)
    processor = FileProcessor(folder_path)
    processor.process_files(tokenizer)
    print(indexer.get_token_info("семья"))

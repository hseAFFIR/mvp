from affir_mvp.modules.tokenizer_factory import TokenizerFactory
from affir_mvp.strategy import Strategy
from affir_mvp.modules.file_reader import FileProcessor
import os

if __name__ == "__main__":
    root_path = os.path.dirname(os.path.dirname(__file__))
    folder_path = os.path.join(root_path, "data")
    factory = TokenizerFactory()
    tokenizer = factory.create_pipeline(Strategy.HIGH)
    processor = FileProcessor(folder_path, tokenizer)
    
    # Вывод
    for file_id, tokens in processor.process_files():
        print(f"ID файла: {file_id}")
        print(f"Токены: {tokens}")
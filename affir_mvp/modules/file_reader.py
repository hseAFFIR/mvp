import os
from affir_mvp.modules.tokenizer_factory import TokenizerFactory
from affir_mvp.strategy import Strategy


class FileProcessor:
    def __init__(self, folder_path: str, tokenizer):
        """
        Класс для последовательной обработки файлов в указанной папке.

        :param folder_path: Путь к папке с файлами.
        :param tokenizer: Экземпляр TokenizerPipeline.
        """
        self.folder_path = folder_path
        self.tokenizer = tokenizer
        self.files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        self.file_map = {file_name: idx + 1 for idx, file_name in enumerate(self.files)}

    def process_files(self):
        """
        Обрабатывает каждый файл последовательно, передавая его содержимое в токенизатор.

        :yield: Кортеж (ID файла, токены).
        """
        for file_name in self.files:
            file_id = f"{file_name}:{self.file_map[file_name]}"
            file_path = os.path.join(self.folder_path, file_name)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                tokens = self.tokenizer.run(content)  # Передаём содержимое в токенизатор
                yield file_id, tokens  # Возвращаем ID файла и токены

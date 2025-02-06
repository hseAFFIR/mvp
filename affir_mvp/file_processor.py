from os import listdir, path

from affir_mvp.tokenizer import TokenizerPipeline


class FileProcessor:
    def __init__(self, folder_path: str):
        """
        Класс для последовательной обработки файлов в указанной папке.

        :param folder_path: Путь к папке с файлами.
        """
        self.folder_path = folder_path
        self.files = [f for f in listdir(folder_path) if f.endswith(".txt")]
        self.file_map = {file_name: idx + 1 for idx, file_name in enumerate(self.files)}

    def process_files(self, tokenizer: TokenizerPipeline):
        """
        Обрабатывает каждый файл последовательно, передавая его содержимое в токенизатор.
        """
        for file_name in self.files:
            file_id = f"{file_name}"
            file_path = path.join(self.folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                tokenizer.run(content, file_id)

from .filters.base import Base


class TokenizerPipeline:
    def __init__(self):
        self.stages = []

    def run(self, text: str) -> list[str]:
        tokens = self._tokenize(text)
        return self.apply_stages(tokens)

    def _tokenize(self, text: str) -> list[str]:
        return text.split()

    def add_stage(self, stage: Base):
        self.stages.append(stage)

    def apply_stages(self, tokens: list[str]) -> list[str]:
        for stage in self.stages:
            stage: Base
            tokens = stage.process(tokens)
        return tokens

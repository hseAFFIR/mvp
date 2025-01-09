from .filters.base import Base


class TokenizerPipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage: Base):
        self.stages.append(stage)

    def process(self, tokens: str) -> list[str]:
        for stage in self.stages:
            tokens = stage.process(tokens)
        return tokens

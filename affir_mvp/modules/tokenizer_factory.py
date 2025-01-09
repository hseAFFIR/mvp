from affir_mvp.strategy import Strategy

from . import filters
from .tokenizer_pipeline import TokenizerPipeline


class TokenizerFactory:
    def create_pipeline(self, strategy: Strategy) -> TokenizerPipeline:
        pipeline = TokenizerPipeline()

        if Strategy.LOW <= strategy:
            pipeline.add_stage(filters.Punctuator())
        if Strategy.HIGH <= strategy:
            pipeline.add_stage(filters.Lowercaser())
        return pipeline

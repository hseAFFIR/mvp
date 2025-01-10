from affir_mvp.strategy import Strategy

from . import filters
from .tokenizer_pipeline import TokenizerPipeline


class TokenizerFactory:

    @staticmethod
    def create_pipeline(strategy: Strategy) -> TokenizerPipeline:
        pipeline = TokenizerPipeline()

        if Strategy.LOW <= strategy:
            pipeline.add_filter(filters.Punctuator())
        if Strategy.HIGH <= strategy:
            pipeline.add_filter(filters.Lowercaser())
        return pipeline

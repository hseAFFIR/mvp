from affir_mvp.strategy import Strategy

from . import filters
from .pipeline import TokenizerPipeline


class TokenizerFactory:

    @staticmethod
    def create_pipeline(strategy: Strategy) -> TokenizerPipeline:
        pipeline = TokenizerPipeline()

        if Strategy.LOW <= strategy:
            pipeline.add_filter(filters.Lowercaser())
        if Strategy.MEDIUM <= strategy:
            pipeline.add_filter(filters.Htmler())
        if Strategy.HIGH <= strategy:
            pipeline.add_filter(filters.Punctuator())
        return pipeline

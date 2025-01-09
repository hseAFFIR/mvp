from affir_mvp.strategy import Strategy

from . import filters
from .tokenizer_pipeline import TokenizerPipeline


class TokenizerFactory:
    def create_pipeline(self, strategy: Strategy) -> TokenizerPipeline:
        pipeline = TokenizerPipeline()

        if Strategy.BASIC <= strategy:
            pipeline.add_stage(filters.Splitter())
        if Strategy.FULL <= strategy:
            pipeline.add_stage(filters.Lowercaser())
        return pipeline

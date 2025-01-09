from affir_mvp.modules.tokenizer_factory import TokenizerFactory
from affir_mvp.strategy import Strategy

if __name__ == "__main__":
    factory = TokenizerFactory()
    tokenizer = factory.create_pipeline(Strategy.FULL)
    print(tokenizer.process(["Проверка текста"]))

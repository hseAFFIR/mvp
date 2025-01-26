import pytest

from affir_mvp.tokenizer.filters import Htmler
from affir_mvp.tokenizer.pipeline import TokenizerPipeline


# Тест без фильтра Htmler
def test_tokenizer_without_htmler():
    tokenizer = TokenizerPipeline()  # без Htmler
    word = "Hello World!"
    filtered_token = tokenizer.apply_filters(word)
    # Ожидаем, что токен останется без изменений
    assert filtered_token == word


@pytest.mark.parametrize(
    "word, expected_output",
    [
        ("<div>", None),  # строка с тегами и длиной меньше 10
        (
            '<img src="1/2/3/4/5/6/7/8/9/10">',
            '<img src="1/2/3/4/5/6/7/8/9/10">',
        ),  # строка с тегами и длиной больше 10
    ],
)
def test_tokenizer_with_htmler(word, expected_output):
    tokenizer = TokenizerPipeline(Htmler())  # с Htmler
    filtered_token = tokenizer.apply_filters(word)
    assert filtered_token == expected_output

import pytest

from affir_mvp.tokenizer.pipeline import TokenizerPipeline


@pytest.fixture
def tokenizer():
    """Фикстура для создания экземпляра TokenizerPipeline."""
    return TokenizerPipeline()


def test_simple_text(tokenizer):
    """Тестирование простого текста."""
    text = "Hello world"
    tokens = list(tokenizer._tokenize(text))
    assert [t.body for t in tokens] == ["Hello", "world"]


def test_text_with_punctuation(tokenizer):
    """Тестирование текста с пунктуацией."""
    text = "говорит: - Давайте будем на ты. - Хорошо, ваше высочество."
    tokens = list(tokenizer._tokenize(text))
    assert [t.body for t in tokens] == [
        "говорит",
        ":",
        "-",
        "Давайте",
        "будем",
        "на",
        "ты",
        ".",
        "-",
        "Хорошо",
        ",",
        "ваше",
        "высочество",
        ".",
    ]


def test_text_with_html(tokenizer):
    """Тестирование текста с HTML тегами."""
    text = "<b>Hello</b> world"
    tokens = list(tokenizer._tokenize(text))
    assert [t.body for t in tokens] == ["<b>", "Hello", "</b>", "world"]


def test_text_with_special_characters(tokenizer):
    """Тестирование текста с особыми символами."""
    text = "Price is $100 @ store."
    tokens = list(tokenizer._tokenize(text))
    assert [t.body for t in tokens] == ["Price", "is", "$", "100", "@", "store", "."]


def test_text_with_multiple_spaces(tokenizer):
    """Тестирование текста с несколькими пробелами."""
    text = "   Hello   world  "
    tokens = list(tokenizer._tokenize(text))
    assert [t.body for t in tokens] == ["Hello", "world"]


def test_empty_text(tokenizer):
    """Тестирование пустого текста."""
    text = ""
    tokens = list(tokenizer._tokenize(text))
    assert tokens == []


def test_only_html(tokenizer):
    """Тестирование только HTML текста."""
    text = "<div><p>Text</p></div>"
    tokens = list(tokenizer._tokenize(text))
    assert [t.body for t in tokens] == ["<div>", "<p>", "Text", "</p>", "</div>"]

import pytest

from affir_mvp.tokenizer.filters import Punctuator
from affir_mvp.tokenizer.pipeline import TokenizerPipeline


@pytest.fixture
def tokenizer():
    """Фикстура для создания экземпляра TokenizerPipeline с фильтром Punctuator."""
    return TokenizerPipeline(Punctuator())


def test_remove_exclamation(tokenizer):
    """Тест на удаление восклицательного знака."""
    word = "Hello World!"
    tokens = tokenizer.run(word)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == ["Hello", "World"]


def test_remove_multiple_punctuation(tokenizer):
    """Тест на удаление нескольких восклицательных знаков."""
    word = "Hello World!!!"
    tokens = tokenizer.run(word)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == ["Hello", "World"]


def test_remove_period(tokenizer):
    """Тест на удаление точки."""
    word = "Hello World."
    tokens = tokenizer.run(word)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == ["Hello", "World"]


def test_remove_comma(tokenizer):
    """Тест на удаление запятой."""
    word = "Hello, World"
    tokens = tokenizer.run(word)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == ["Hello", "World"]


def test_no_change_for_alphanumeric(tokenizer):
    """Тест, который проверяет, что алфавитные символы остаются неизменными."""
    word = "Hello World"
    tokens = tokenizer.run(word)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == ["Hello", "World"]


def test_no_change_for_question_mark(tokenizer):
    """Тест на отсутствие изменений для вопросительного знака."""
    word = "Hello World?"
    tokens = tokenizer.run(word)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == ["Hello", "World"]


def test_text_with_punctuation(tokenizer):
    """Тест на обработку текста с различными знаками препинания."""
    text = (
        "Доброго дня, всем новоприбывшим, меня зовут Серегей К., "
        "я учусь на первом курсе магистратуры (очного отд.) фак. РТС "
        "так же я прохожу курсы английского языка в ЦОИЯ "
        "(3-ий уровень) у Белынцевой Светланы Николаевны. В данном блоге "
        "я постараюсь постить самую полезную и необходимую информацию "
        "касающуюся этих двух направлений обучения."
    )
    tokens = tokenizer.run(text)
    token_bodies = [token.body for token in tokens]
    assert token_bodies == [
        "Доброго",
        "дня",
        "всем",
        "новоприбывшим",
        "меня",
        "зовут",
        "Серегей",
        "К",
        "я",
        "учусь",
        "на",
        "первом",
        "курсе",
        "магистратуры",
        "очного",
        "отд",
        "фак",
        "РТС",
        "так",
        "же",
        "я",
        "прохожу",
        "курсы",
        "английского",
        "языка",
        "в",
        "ЦОИЯ",
        "3",
        "ий",
        "уровень",
        "у",
        "Белынцевой",
        "Светланы",
        "Николаевны",
        "В",
        "данном",
        "блоге",
        "я",
        "постараюсь",
        "постить",
        "самую",
        "полезную",
        "и",
        "необходимую",
        "информацию",
        "касающуюся",
        "этих",
        "двух",
        "направлений",
        "обучения",
    ]


from SanskritAI.domain.lexical.lemma import Lemma
from SanskritAI.domain.lexical.token import Token
from SanskritAI.domain.lexical.word_form import WordForm


def make_lemma():
    return Lemma(
        identifier="lemma-001",
        text="राम",
        transliteration="rāma",
    )


def make_word_form(
    text="रामः",
):
    return WordForm(
        identifier="word-form-001",
        lemma=make_lemma(),
        text=text,
    )


def make_token(
    text="रामः",
    position=0,
    description="",
):
    return Token(
        identifier="token-001",
        word_form=make_word_form(text=text),
        text=text,
        position=position,
        description=description,
    )


def test_token_can_be_created():
    token = make_token()

    assert token.identifier == "token-001"
    assert token.text == "रामः"
    assert token.position == 0
    assert token.description == ""


def test_token_preserves_word_form():
    word_form = make_word_form()

    token = Token(
        identifier="token-001",
        word_form=word_form,
        text="रामः",
    )

    assert token.word_form is word_form


def test_token_preserves_position():
    token = make_token(position=5)

    assert token.position == 5


def test_token_preserves_description():
    token = make_token(
        description="First token",
    )

    assert token.description == "First token"


def test_display_name():
    token = make_token()

    assert token.display_name == "रामः"


def test_display_text():
    token = make_token()

    assert token.display_text == "रामः"


def test_display_description():
    token = make_token(
        description="First token",
    )

    assert token.display_description == "First token"


def test_lemma_delegates_to_word_form():
    token = make_token()

    assert token.lemma is token.word_form.lemma
    assert token.lemma.text == "राम"


def test_canonical_form_delegates_to_word_form():
    token = make_token()

    assert token.canonical_form == "राम"


def test_is_lemma_delegates_to_word_form():
    non_lemma_token = make_token(text="रामः")

    assert non_lemma_token.is_lemma is False


def test_token_using_lemma_form():
    token = make_token(text="राम")

    assert token.is_lemma is True
    assert token.canonical_form == "राम"


def test_string_representation():
    token = make_token()

    assert str(token) == "रामः"


def test_token_is_immutable():
    token = make_token()

    try:
        token.text = "हरिः"
        assert False, "Token should be immutable"
    except AttributeError:
        pass


def test_token_is_immutable_for_position():
    token = make_token()

    try:
        token.position = 10
        assert False, "Token should be immutable"
    except AttributeError:
        pass


from SanskritAI.domain.lexical.token import Token
from SanskritAI.domain.lexical.word_form import WordForm


def make_word_form():
    return WordForm(
        identifier="wf-001",
        text="रामः",
    )


def test_token_can_be_created():
    word_form = make_word_form()

    token = Token(
        identifier="token-001",
        word_form=word_form,
        text="रामः",
    )

    assert token.identifier == "token-001"
    assert token.word_form is word_form
    assert token.text == "रामः"
    assert token.position == 0
    assert token.description == ""


def test_token_preserves_position():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
        position=5,
    )

    assert token.position == 5


def test_token_preserves_description():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
        description="First token",
    )

    assert token.description == "First token"


def test_display_name():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
    )

    assert token.display_name == "रामः"


def test_display_text():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
    )

    assert token.display_text == "रामः"


def test_display_description():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
        description="First token",
    )

    assert token.display_description == "First token"


def test_lemma_delegates_to_word_form():
    word_form = make_word_form()

    token = Token(
        identifier="token-001",
        word_form=word_form,
        text="रामः",
    )

    assert token.lemma == word_form.lemma


def test_canonical_form_delegates_to_word_form():
    word_form = make_word_form()

    token = Token(
        identifier="token-001",
        word_form=word_form,
        text="रामः",
    )

    assert token.canonical_form == word_form.canonical_form


def test_is_lemma_delegates_to_word_form():
    word_form = make_word_form()

    token = Token(
        identifier="token-001",
        word_form=word_form,
        text="रामः",
    )

    assert token.is_lemma == word_form.is_lemma


def test_string_representation():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
    )

    assert str(token) == "रामः"


def test_token_is_immutable():
    token = Token(
        identifier="token-001",
        word_form=make_word_form(),
        text="रामः",
    )

    try:
        token.text = "हरिः"
        assert False, "Token should be immutable"
    except AttributeError:
        pass

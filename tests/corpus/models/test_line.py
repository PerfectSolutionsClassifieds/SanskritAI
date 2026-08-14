
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.line_metadata import LineMetadata
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.token_metadata import TokenMetadata


def make_line(identifier="line-1"):
    return Line(
        identifier=identifier,
        metadata=LineMetadata(),
    )


def make_token(identifier="token-1", text="रामः"):
    return Token(
        identifier=identifier,
        metadata=TokenMetadata(text=text),
    )


def test_line_stores_identifier():
    line = make_line()

    assert line.id == "line-1"


def test_line_stores_metadata():
    metadata = LineMetadata()

    line = Line(
        identifier="line-1",
        metadata=metadata,
    )

    assert line.metadata is metadata


def test_line_starts_without_tokens():
    line = make_line()

    assert line.tokens == []
    assert line.token_count == 0


def test_tokens_alias_children():
    line = make_line()

    assert line.tokens is line.children


def test_add_token():
    line = make_line()
    token = make_token()

    line.add_token(token)

    assert line.tokens == [token]
    assert line.token_count == 1


def test_remove_token():
    line = make_line()
    token = make_token()

    line.add_token(token)
    line.remove_token(token)

    assert line.tokens == []
    assert line.token_count == 0


def test_first_token():
    line = make_line()

    first = make_token("token-1", "रामः")
    second = make_token("token-2", "गच्छति")

    line.add_token(first)
    line.add_token(second)

    assert line.first_token is first


def test_last_token():
    line = make_line()

    first = make_token("token-1", "रामः")
    second = make_token("token-2", "गच्छति")

    line.add_token(first)
    line.add_token(second)

    assert line.last_token is second


def test_tokens_preserve_insertion_order():
    line = make_line()

    tokens = [
        make_token("token-1", "रामः"),
        make_token("token-2", "वनम्"),
        make_token("token-3", "गच्छति"),
    ]

    for token in tokens:
        line.add_token(token)

    assert line.tokens == tokens


def test_line_number_aliases_metadata():
    metadata = LineMetadata(line_number=7)

    line = Line(
        identifier="line-1",
        metadata=metadata,
    )

    assert line.line_number == 7


def test_language_aliases_metadata():
    metadata = LineMetadata(language="sanskrit")

    line = Line(
        identifier="line-1",
        metadata=metadata,
    )

    assert line.language == "sanskrit"

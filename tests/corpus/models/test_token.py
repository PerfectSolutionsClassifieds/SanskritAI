
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.token_metadata import TokenMetadata


def make_token(
    identifier="token-1",
    text="रामः",
    normalized_text="रामः",
):
    return Token(
        identifier=identifier,
        metadata=TokenMetadata(
            text=text,
            normalized_text=normalized_text,
        ),
    )


def test_token_stores_identifier():
    token = make_token()

    assert token.id == "token-1"


def test_token_stores_metadata():
    metadata = TokenMetadata(
        text="रामः",
        normalized_text="रामः",
    )

    token = Token(
        identifier="token-1",
        metadata=metadata,
    )

    assert token.metadata is metadata


def test_token_is_a_base_node():
    from SanskritAI.corpus.models.base_node import BaseNode

    token = make_token()

    assert isinstance(token, BaseNode)


def test_token_is_leaf_node():
    token = make_token()

    assert not hasattr(token, "children")


def test_token_text_aliases_metadata():
    token = make_token(text="रामः")

    assert token.text == "रामः"


def test_token_normalized_text_aliases_metadata():
    token = make_token(
        text="रामः",
        normalized_text="राम",
    )

    assert token.normalized_text == "राम"


def test_token_preserves_original_and_normalized_text():
    token = make_token(
        text="रामः",
        normalized_text="राम",
    )

    assert token.text == "रामः"
    assert token.normalized_text == "राम"


def test_token_metadata_is_accessible():
    token = make_token()

    assert token.metadata.text == "रामः"
    assert token.metadata.normalized_text == "रामः"

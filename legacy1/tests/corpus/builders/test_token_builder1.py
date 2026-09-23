
from SanskritAI.corpus.builders.token_builder import TokenBuilder
from SanskritAI.corpus.enums.token_type import TokenType
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.token_metadata import TokenMetadata


def test_create_instance_returns_token():
    token = TokenBuilder().build()

    assert isinstance(token, Token)


def test_create_instance_initializes_metadata():
    token = TokenBuilder().build()

    assert isinstance(token.metadata, TokenMetadata)


def test_create_instance_generates_identifier():
    first = TokenBuilder().build()
    second = TokenBuilder().build()

    assert first.identifier is not None
    assert second.identifier is not None
    assert first.identifier != second.identifier


def test_token_is_leaf():
    token = TokenBuilder().build()

    assert token.child_count == 0


def test_with_text_is_fluent():
    builder = TokenBuilder()

    result = builder.with_text("रामः")

    assert result is builder


def test_with_normalized_text_is_fluent():
    builder = TokenBuilder()

    result = builder.with_normalized_text("रामः")

    assert result is builder


def test_with_position_is_fluent():
    builder = TokenBuilder()

    result = builder.with_position(1)

    assert result is builder


def test_with_token_type_is_fluent():
    builder = TokenBuilder()

    result = builder.with_token_type(TokenType.WORD)

    assert result is builder


def test_with_confidence_is_fluent():
    builder = TokenBuilder()

    result = builder.with_confidence(0.95)

    assert result is builder


def test_with_source_offset_is_fluent():
    builder = TokenBuilder()

    result = builder.with_source_offset(10)

    assert result is builder


def test_with_text_sets_metadata():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .build()
    )

    assert token.metadata.text == "रामः"


def test_with_normalized_text_sets_metadata():
    token = (
        TokenBuilder()
        .with_normalized_text("राम")
        .build()
    )

    assert token.metadata.normalized_text == "राम"


def test_with_position_sets_metadata():
    token = (
        TokenBuilder()
        .with_position(5)
        .build()
    )

    assert token.metadata.position == 5


def test_with_token_type_sets_metadata():
    token = (
        TokenBuilder()
        .with_token_type(TokenType.WORD)
        .build()
    )

    assert token.metadata.token_type == TokenType.WORD


def test_with_confidence_sets_metadata():
    token = (
        TokenBuilder()
        .with_confidence(0.875)
        .build()
    )

    assert token.metadata.confidence == 0.875


def test_with_source_offset_sets_metadata():
    token = (
        TokenBuilder()
        .with_source_offset(42)
        .build()
    )

    assert token.metadata.source_offset == 42


def test_build_supports_complete_token_definition():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .with_normalized_text("राम")
        .with_position(1)
        .with_token_type(TokenType.WORD)
        .with_confidence(0.99)
        .with_source_offset(12)
        .build()
    )

    assert token.metadata.text == "रामः"
    assert token.metadata.normalized_text == "राम"
    assert token.metadata.position == 1
    assert token.metadata.token_type == TokenType.WORD
    assert token.metadata.confidence == 0.99
    assert token.metadata.source_offset == 12


def test_build_returns_independent_copy():
    builder = (
        TokenBuilder()
        .with_text("रामः")
    )

    first = builder.build()

    first.metadata.text = "बदल"

    second = builder.build()

    assert second.metadata.text == "रामः"


def test_reset_creates_fresh_token():
    builder = (
        TokenBuilder()
        .with_text("रामः")
    )

    first = builder.build()

    builder.reset()

    second = builder.build()

    assert second is not first
    assert second.metadata.text != "रामः"


def test_reset_clears_metadata():
    builder = (
        TokenBuilder()
        .with_text("रामः")
        .with_position(1)
    )

    builder.reset()

    token = builder.build()

    assert token.metadata.text is None
    assert token.metadata.position is None


def test_from_token_returns_builder():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .with_position(1)
        .build()
    )

    builder = TokenBuilder.from_token(token)

    assert isinstance(builder, TokenBuilder)


def test_from_token_copies_metadata():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .with_normalized_text("राम")
        .with_position(1)
        .with_token_type(TokenType.WORD)
        .with_confidence(0.95)
        .with_source_offset(10)
        .build()
    )

    rebuilt = TokenBuilder.from_token(token).build()

    assert rebuilt.metadata.text == "रामः"
    assert rebuilt.metadata.normalized_text == "राम"
    assert rebuilt.metadata.position == 1
    assert rebuilt.metadata.token_type == TokenType.WORD
    assert rebuilt.metadata.confidence == 0.95
    assert rebuilt.metadata.source_offset == 10


def test_from_token_does_not_alias_original():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .build()
    )

    rebuilt = TokenBuilder.from_token(token).build()

    rebuilt.metadata.text = "बदल"

    assert token.metadata.text == "रामः"

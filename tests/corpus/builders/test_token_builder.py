
from SanskritAI.corpus.builders.token_builder import TokenBuilder
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.token_metadata import TokenMetadata
from SanskritAI.corpus.enums.token_type import TokenType


def first_enum_member(enum_class):
    return next(iter(enum_class))


def test_create_instance_returns_token():
    token = TokenBuilder().build()

    assert isinstance(token, Token)


def test_create_instance_initializes_metadata():
    token = TokenBuilder().build()

    assert isinstance(token.metadata, TokenMetadata)


def test_create_instance_generates_identifier():
    first = TokenBuilder().build()
    second = TokenBuilder().build()

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_text_is_fluent():
    builder = TokenBuilder()

    result = builder.with_text("रामः")

    assert result is builder


def test_with_text_sets_metadata():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .build()
    )

    assert token.metadata.text == "रामः"
    assert token.text == "रामः"


def test_with_normalized_text_is_fluent():
    builder = TokenBuilder()

    result = builder.with_normalized_text("राम")

    assert result is builder


def test_with_normalized_text_sets_metadata():
    token = (
        TokenBuilder()
        .with_normalized_text("राम")
        .build()
    )

    assert token.metadata.normalized_text == "राम"
    assert token.normalized_text == "राम"


def test_with_position_is_fluent():
    builder = TokenBuilder()

    result = builder.with_position(3)

    assert result is builder


def test_with_position_sets_metadata():
    token = (
        TokenBuilder()
        .with_position(3)
        .build()
    )

    assert token.metadata.position == 3
    assert token.position == 3


def test_with_token_type_is_fluent():
    builder = TokenBuilder()
    value = first_enum_member(TokenType)

    result = builder.with_token_type(value)

    assert result is builder


def test_with_token_type_sets_metadata():
    value = first_enum_member(TokenType)

    token = (
        TokenBuilder()
        .with_token_type(value)
        .build()
    )

    assert token.metadata.token_type == value
    assert token.token_type == value


def test_with_confidence_is_fluent():
    builder = TokenBuilder()

    result = builder.with_confidence(0.95)

    assert result is builder


def test_with_confidence_sets_metadata():
    token = (
        TokenBuilder()
        .with_confidence(0.95)
        .build()
    )

    assert token.metadata.confidence == 0.95


def test_with_source_offset_is_fluent():
    builder = TokenBuilder()

    result = builder.with_source_offset(42)

    assert result is builder


def test_with_source_offset_sets_metadata():
    token = (
        TokenBuilder()
        .with_source_offset(42)
        .build()
    )

    assert token.metadata.source_offset == 42


def test_build_returns_independent_copy():
    builder = TokenBuilder().with_text("रामः")

    first = builder.build()

    builder.with_text("सीता")

    second = builder.build()

    assert first.text == "रामः"
    assert second.text == "सीता"


def test_reset_creates_fresh_token():
    builder = TokenBuilder().with_text("रामः")

    original_id = builder.build().id

    builder.reset()

    fresh = builder.build()

    assert isinstance(fresh, Token)
    assert fresh.id != original_id
    assert fresh.metadata.text is None


def test_from_token_returns_builder():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .build()
    )

    builder = TokenBuilder.from_token(token)

    assert isinstance(builder, TokenBuilder)


def test_from_token_copies_metadata():
    value = first_enum_member(TokenType)

    token = (
        TokenBuilder()
        .with_text("रामः")
        .with_normalized_text("राम")
        .with_position(1)
        .with_token_type(value)
        .with_confidence(0.95)
        .with_source_offset(42)
        .build()
    )

    copied = TokenBuilder.from_token(token).build()

    assert copied.metadata.text == "रामः"
    assert copied.metadata.normalized_text == "राम"
    assert copied.metadata.position == 1
    assert copied.metadata.token_type == value
    assert copied.metadata.confidence == 0.95
    assert copied.metadata.source_offset == 42


def test_from_token_does_not_alias_original():
    token = (
        TokenBuilder()
        .with_text("रामः")
        .build()
    )

    copied = TokenBuilder.from_token(token).build()

    copied.metadata.text = "सीता"

    assert token.text == "रामः"
    assert copied.text == "सीता"

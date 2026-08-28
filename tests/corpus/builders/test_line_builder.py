
from SanskritAI.corpus.builders.line_builder import LineBuilder
from SanskritAI.corpus.builders.token_builder import TokenBuilder
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.line_metadata import LineMetadata


def make_line(number=1):
    return (
        LineBuilder()
        .with_line_number(number)
        .build()
    )


def make_token(text="रामः", position=1):
    return (
        TokenBuilder()
        .with_text(text)
        .with_position(position)
        .build()
    )


def test_create_instance_returns_line():
    line = LineBuilder().build()

    assert isinstance(line, Line)


def test_create_instance_initializes_metadata():
    line = LineBuilder().build()

    assert isinstance(line.metadata, LineMetadata)


def test_create_instance_generates_identifier():
    first = LineBuilder().build()
    second = LineBuilder().build()

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_line_number_is_fluent():
    builder = LineBuilder()

    result = builder.with_line_number(3)

    assert result is builder


def test_with_line_number_sets_metadata():
    line = (
        LineBuilder()
        .with_line_number(3)
        .build()
    )

    assert line.metadata.line_number == 3


def test_with_visual_line_number_is_fluent():
    builder = LineBuilder()

    result = builder.with_visual_line_number(7)

    assert result is builder


def test_with_visual_line_number_sets_metadata():
    line = (
        LineBuilder()
        .with_visual_line_number(7)
        .build()
    )

    assert line.metadata.visual_line_number == 7


def test_with_visual_line_number_accepts_none():
    line = (
        LineBuilder()
        .with_visual_line_number(None)
        .build()
    )

    assert line.metadata.visual_line_number is None


def test_with_pada_number_is_fluent():
    builder = LineBuilder()

    result = builder.with_pada_number(2)

    assert result is builder


def test_with_pada_number_sets_metadata():
    line = (
        LineBuilder()
        .with_pada_number(2)
        .build()
    )

    assert line.metadata.pada_number == 2


def test_with_pada_number_accepts_none():
    line = (
        LineBuilder()
        .with_pada_number(None)
        .build()
    )

    assert line.metadata.pada_number is None


def test_with_indentation_is_fluent():
    builder = LineBuilder()

    result = builder.with_indentation(3)

    assert result is builder


def test_with_indentation_sets_metadata():
    line = (
        LineBuilder()
        .with_indentation(3)
        .build()
    )

    assert line.metadata.indentation_level == 3


def test_as_continuation_is_fluent():
    builder = LineBuilder()

    result = builder.as_continuation()

    assert result is builder


def test_as_continuation_sets_metadata():
    line = (
        LineBuilder()
        .as_continuation()
        .build()
    )

    assert line.metadata.is_continuation is True


def test_as_continuation_accepts_false():
    line = (
        LineBuilder()
        .as_continuation(False)
        .build()
    )

    assert line.metadata.is_continuation is False


def test_add_token_is_fluent():
    token = make_token()

    builder = LineBuilder()

    result = builder.add_token(token)

    assert result is builder


def test_add_token_adds_child():
    token = make_token()

    line = (
        LineBuilder()
        .add_token(token)
        .build()
    )

    assert len(line.tokens) == 1
    assert line.tokens[0] == token


def test_add_tokens_adds_all_children():
    tokens = [
        make_token("रामः", 1),
        make_token("वनम्", 2),
        make_token("गच्छति", 3),
    ]

    line = (
        LineBuilder()
        .add_tokens(tokens)
        .build()
    )

    assert len(line.tokens) == 3
    assert line.tokens == tokens


def test_add_tokens_preserves_order():
    tokens = [
        make_token("प्रथमः", 1),
        make_token("द्वितीयः", 2),
        make_token("तृतीयः", 3),
    ]

    line = (
        LineBuilder()
        .add_tokens(tokens)
        .build()
    )

    assert line.tokens[0] == tokens[0]
    assert line.tokens[1] == tokens[1]
    assert line.tokens[2] == tokens[2]


def test_build_returns_independent_copy():
    builder = LineBuilder().with_line_number(1)

    first = builder.build()

    builder.with_line_number(2)

    second = builder.build()

    assert first.metadata.line_number == 1
    assert second.metadata.line_number == 2


def test_reset_creates_fresh_line():
    builder = LineBuilder().with_line_number(1)

    original_id = builder.build().id

    builder.reset()

    fresh = builder.build()

    assert isinstance(fresh, Line)
    assert fresh.id != original_id
    assert fresh.metadata.line_number is None


def test_reset_clears_tokens():
    token = make_token()

    builder = LineBuilder().add_token(token)

    assert len(builder.instance().tokens) == 1

    builder.reset()

    assert len(builder.instance().tokens) == 0


def test_from_line_returns_builder():
    line = make_line(5)

    builder = LineBuilder.from_line(line)

    assert isinstance(builder, LineBuilder)


def test_from_line_copies_metadata():
    line = (
        LineBuilder()
        .with_line_number(5)
        .with_visual_line_number(8)
        .with_pada_number(2)
        .with_indentation(3)
        .as_continuation()
        .build()
    )

    copied = LineBuilder.from_line(line).build()

    assert copied.metadata.line_number == 5
    assert copied.metadata.visual_line_number == 8
    assert copied.metadata.pada_number == 2
    assert copied.metadata.indentation_level == 3
    assert copied.metadata.is_continuation is True


def test_from_line_does_not_alias_original():
    line = (
        LineBuilder()
        .with_line_number(1)
        .build()
    )

    copied = LineBuilder.from_line(line).build()

    copied.metadata.line_number = 2

    assert line.metadata.line_number == 1
    assert copied.metadata.line_number == 2

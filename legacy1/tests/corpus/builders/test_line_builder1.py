
from SanskritAI.corpus.builders.line_builder import LineBuilder
from SanskritAI.corpus.builders.token_builder import TokenBuilder
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.line_metadata import LineMetadata


def make_token(text: str = "रामः"):
    return (
        TokenBuilder()
        .with_text(text)
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

    assert first.identifier is not None
    assert second.identifier is not None
    assert first.identifier != second.identifier


def test_with_line_number_is_fluent():
    builder = LineBuilder()

    result = builder.with_line_number(1)

    assert result is builder


def test_with_visual_line_number_is_fluent():
    builder = LineBuilder()

    result = builder.with_visual_line_number(2)

    assert result is builder


def test_with_pada_number_is_fluent():
    builder = LineBuilder()

    result = builder.with_pada_number(1)

    assert result is builder


def test_with_indentation_is_fluent():
    builder = LineBuilder()

    result = builder.with_indentation(4)

    assert result is builder


def test_as_continuation_is_fluent():
    builder = LineBuilder()

    result = builder.as_continuation()

    assert result is builder


def test_with_line_number_sets_metadata():
    line = (
        LineBuilder()
        .with_line_number(7)
        .build()
    )

    assert line.metadata.line_number == 7


def test_with_visual_line_number_sets_metadata():
    line = (
        LineBuilder()
        .with_visual_line_number(8)
        .build()
    )

    assert line.metadata.visual_line_number == 8


def test_with_pada_number_sets_metadata():
    line = (
        LineBuilder()
        .with_pada_number(3)
        .build()
    )

    assert line.metadata.pada_number == 3


def test_with_visual_line_number_accepts_none():
    line = (
        LineBuilder()
        .with_visual_line_number(None)
        .build()
    )

    assert line.metadata.visual_line_number is None


def test_with_pada_number_accepts_none():
    line = (
        LineBuilder()
        .with_pada_number(None)
        .build()
    )

    assert line.metadata.pada_number is None


def test_with_indentation_sets_metadata():
    line = (
        LineBuilder()
        .with_indentation(4)
        .build()
    )

    assert line.metadata.indentation_level == 4


def test_as_continuation_sets_flag():
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

    assert line.child_count == 1
    assert line.first_child is token


def test_add_tokens_adds_all_children():
    tokens = [
        make_token("रामः"),
        make_token("वनम्"),
        make_token("गच्छति"),
    ]

    line = (
        LineBuilder()
        .add_tokens(tokens)
        .build()
    )

    assert line.child_count == 3
    assert list(line) == tokens


def test_add_tokens_accepts_iterable():
    tokens = (
        make_token("रामः"),
        make_token("वनम्"),
    )

    line = (
        LineBuilder()
        .add_tokens(iter(tokens))
        .build()
    )

    assert line.child_count == 2
    assert list(line) == list(tokens)


def test_build_returns_independent_copy():
    builder = (
        LineBuilder()
        .with_line_number(1)
    )

    first = builder.build()

    first.metadata.line_number = 99

    second = builder.build()

    assert second.metadata.line_number == 1


def test_reset_creates_fresh_line():
    builder = (
        LineBuilder()
        .with_line_number(1)
    )

    first = builder.build()

    builder.reset()

    second = builder.build()

    assert second is not first
    assert second.metadata.line_number != 1


def test_reset_clears_children():
    token = make_token()

    builder = (
        LineBuilder()
        .add_token(token)
    )

    builder.reset()

    line = builder.build()

    assert line.child_count == 0


def test_from_line_returns_builder():
    line = (
        LineBuilder()
        .with_line_number(10)
        .with_indentation(2)
        .build()
    )

    builder = LineBuilder.from_line(line)

    assert isinstance(builder, LineBuilder)


def test_from_line_copies_metadata():
    line = (
        LineBuilder()
        .with_line_number(10)
        .with_visual_line_number(11)
        .with_pada_number(2)
        .with_indentation(4)
        .as_continuation()
        .build()
    )

    rebuilt = LineBuilder.from_line(line).build()

    assert rebuilt.metadata.line_number == 10
    assert rebuilt.metadata.visual_line_number == 11
    assert rebuilt.metadata.pada_number == 2
    assert rebuilt.metadata.indentation_level == 4
    assert rebuilt.metadata.is_continuation is True


def test_from_line_copies_children():
    token = make_token()

    line = (
        LineBuilder()
        .add_token(token)
        .build()
    )

    rebuilt = LineBuilder.from_line(line).build()

    assert rebuilt.child_count == 1
    assert rebuilt.first_child is token


def test_from_line_does_not_alias_original():
    line = (
        LineBuilder()
        .with_line_number(10)
        .build()
    )

    rebuilt = LineBuilder.from_line(line).build()

    rebuilt.metadata.line_number = 20

    assert line.metadata.line_number == 10

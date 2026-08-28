
from SanskritAI.corpus.builders.paragraph_builder import ParagraphBuilder
from SanskritAI.corpus.builders.line_builder import LineBuilder
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata
from SanskritAI.corpus.enums.paragraph_type import ParagraphType


def make_paragraph(number=1):
    return (
        ParagraphBuilder()
        .with_paragraph_number(number)
        .build()
    )


def make_line(number=1):
    return (
        LineBuilder()
        .with_line_number(number)
        .build()
    )


def first_enum_member(enum_class):
    return next(iter(enum_class))


def test_create_instance_returns_paragraph():
    paragraph = ParagraphBuilder().build()

    assert isinstance(paragraph, Paragraph)


def test_create_instance_initializes_metadata():
    paragraph = ParagraphBuilder().build()

    assert isinstance(paragraph.metadata, ParagraphMetadata)


def test_create_instance_generates_identifier():
    first = ParagraphBuilder().build()
    second = ParagraphBuilder().build()

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_paragraph_number_is_fluent():
    builder = ParagraphBuilder()

    result = builder.with_paragraph_number(5)

    assert result is builder


def test_with_paragraph_number_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(5)
        .build()
    )

    assert paragraph.metadata.paragraph_number == 5


def test_with_paragraph_type_is_fluent():
    builder = ParagraphBuilder()
    value = first_enum_member(ParagraphType)

    result = builder.with_paragraph_type(value)

    assert result is builder


def test_with_paragraph_type_sets_metadata():
    value = first_enum_member(ParagraphType)

    paragraph = (
        ParagraphBuilder()
        .with_paragraph_type(value)
        .build()
    )

    assert paragraph.metadata.paragraph_type == value


def test_with_language_variant_is_fluent():
    builder = ParagraphBuilder()

    result = builder.with_language_variant("Telugu")

    assert result is builder


def test_with_language_variant_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .with_language_variant("Telugu")
        .build()
    )

    assert paragraph.metadata.language_variant == "Telugu"


def test_as_translation_is_fluent():
    builder = ParagraphBuilder()

    result = builder.as_translation()

    assert result is builder


def test_as_translation_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .as_translation()
        .build()
    )

    assert paragraph.metadata.is_translation is True


def test_as_translation_accepts_false():
    paragraph = (
        ParagraphBuilder()
        .as_translation(False)
        .build()
    )

    assert paragraph.metadata.is_translation is False


def test_as_commentary_is_fluent():
    builder = ParagraphBuilder()

    result = builder.as_commentary()

    assert result is builder


def test_as_commentary_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .as_commentary()
        .build()
    )

    assert paragraph.metadata.is_commentary is True


def test_as_commentary_accepts_false():
    paragraph = (
        ParagraphBuilder()
        .as_commentary(False)
        .build()
    )

    assert paragraph.metadata.is_commentary is False


def test_add_line_is_fluent():
    line = make_line()

    builder = ParagraphBuilder()

    result = builder.add_line(line)

    assert result is builder


def test_add_line_adds_child():
    line = make_line()

    paragraph = (
        ParagraphBuilder()
        .add_line(line)
        .build()
    )

    assert len(paragraph.lines) == 1
    assert paragraph.lines[0] == line


def test_add_lines_adds_all_children():
    lines = [
        make_line(1),
        make_line(2),
        make_line(3),
    ]

    paragraph = (
        ParagraphBuilder()
        .add_lines(lines)
        .build()
    )

    assert len(paragraph.lines) == 3
    assert paragraph.lines == lines


def test_add_lines_preserves_order():
    lines = [
        make_line(1),
        make_line(2),
        make_line(3),
    ]

    paragraph = (
        ParagraphBuilder()
        .add_lines(lines)
        .build()
    )

    assert paragraph.lines[0] == lines[0]
    assert paragraph.lines[1] == lines[1]
    assert paragraph.lines[2] == lines[2]


def test_build_returns_independent_copy():
    builder = ParagraphBuilder().with_paragraph_number(1)

    first = builder.build()

    builder.with_paragraph_number(2)

    second = builder.build()

    assert first.metadata.paragraph_number == 1
    assert second.metadata.paragraph_number == 2


def test_reset_creates_fresh_paragraph():
    builder = ParagraphBuilder().with_paragraph_number(1)

    original_id = builder.build().id

    builder.reset()

    fresh = builder.build()

    assert isinstance(fresh, Paragraph)
    assert fresh.id != original_id
    assert fresh.metadata.paragraph_number is None


def test_reset_clears_lines():
    line = make_line()

    builder = ParagraphBuilder().add_line(line)

    assert len(builder.instance().lines) == 1

    builder.reset()

    assert len(builder.instance().lines) == 0


def test_from_paragraph_returns_builder():
    paragraph = make_paragraph(7)

    builder = ParagraphBuilder.from_paragraph(paragraph)

    assert isinstance(builder, ParagraphBuilder)


def test_from_paragraph_copies_metadata():
    value = first_enum_member(ParagraphType)

    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(7)
        .with_paragraph_type(value)
        .with_language_variant("Telugu")
        .as_translation()
        .as_commentary(False)
        .build()
    )

    copied = ParagraphBuilder.from_paragraph(paragraph).build()

    assert copied.metadata.paragraph_number == 7
    assert copied.metadata.paragraph_type == value
    assert copied.metadata.language_variant == "Telugu"
    assert copied.metadata.is_translation is True
    assert copied.metadata.is_commentary is False


def test_from_paragraph_does_not_alias_original():
    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(1)
        .build()
    )

    copied = ParagraphBuilder.from_paragraph(paragraph).build()

    copied.metadata.paragraph_number = 2

    assert paragraph.metadata.paragraph_number == 1
    assert copied.metadata.paragraph_number == 2

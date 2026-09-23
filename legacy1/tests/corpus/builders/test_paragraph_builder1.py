
from SanskritAI.corpus.builders.paragraph_builder import ParagraphBuilder
from SanskritAI.corpus.builders.line_builder import LineBuilder
from SanskritAI.corpus.enums.paragraph_type import ParagraphType
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata


def make_line(number: int = 1):
    return (
        LineBuilder()
        .with_line_number(number)
        .build()
    )


def test_create_instance_returns_paragraph():
    paragraph = ParagraphBuilder().build()

    assert isinstance(paragraph, Paragraph)


def test_create_instance_initializes_metadata():
    paragraph = ParagraphBuilder().build()

    assert isinstance(paragraph.metadata, ParagraphMetadata)


def test_create_instance_generates_identifier():
    first = ParagraphBuilder().build()
    second = ParagraphBuilder().build()

    assert first.identifier is not None
    assert second.identifier is not None
    assert first.identifier != second.identifier


def test_with_paragraph_number_is_fluent():
    builder = ParagraphBuilder()

    result = builder.with_paragraph_number(1)

    assert result is builder


def test_with_paragraph_type_is_fluent():
    builder = ParagraphBuilder()

    result = builder.with_paragraph_type(ParagraphType.PROSE)

    assert result is builder


def test_with_language_variant_is_fluent():
    builder = ParagraphBuilder()

    result = builder.with_language_variant("Sanskrit")

    assert result is builder


def test_as_translation_is_fluent():
    builder = ParagraphBuilder()

    result = builder.as_translation()

    assert result is builder


def test_as_commentary_is_fluent():
    builder = ParagraphBuilder()

    result = builder.as_commentary()

    assert result is builder


def test_with_paragraph_number_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(5)
        .build()
    )

    assert paragraph.metadata.paragraph_number == 5


def test_with_paragraph_type_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .with_paragraph_type(ParagraphType.PROSE)
        .build()
    )

    assert paragraph.metadata.paragraph_type == ParagraphType.PROSE


def test_with_language_variant_sets_metadata():
    paragraph = (
        ParagraphBuilder()
        .with_language_variant("Telugu")
        .build()
    )

    assert paragraph.metadata.language_variant == "Telugu"


def test_as_translation_sets_flag():
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


def test_as_commentary_sets_flag():
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

    assert paragraph.child_count == 1
    assert paragraph.first_child is line


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

    assert paragraph.child_count == 3
    assert list(paragraph) == lines


def test_add_lines_accepts_iterable():
    lines = (
        make_line(1),
        make_line(2),
    )

    paragraph = (
        ParagraphBuilder()
        .add_lines(iter(lines))
        .build()
    )

    assert paragraph.child_count == 2
    assert list(paragraph) == list(lines)


def test_build_returns_independent_copy():
    builder = (
        ParagraphBuilder()
        .with_paragraph_number(1)
    )

    first = builder.build()

    first.metadata.paragraph_number = 99

    second = builder.build()

    assert second.metadata.paragraph_number == 1


def test_reset_creates_fresh_paragraph():
    builder = (
        ParagraphBuilder()
        .with_paragraph_number(1)
    )

    first = builder.build()

    builder.reset()

    second = builder.build()

    assert second is not first
    assert second.metadata.paragraph_number != 1


def test_reset_clears_children():
    line = make_line()

    builder = (
        ParagraphBuilder()
        .add_line(line)
    )

    builder.reset()

    paragraph = builder.build()

    assert paragraph.child_count == 0


def test_from_paragraph_returns_builder():
    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(5)
        .with_language_variant("Sanskrit")
        .build()
    )

    builder = ParagraphBuilder.from_paragraph(paragraph)

    assert isinstance(builder, ParagraphBuilder)


def test_from_paragraph_copies_metadata():
    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(5)
        .with_paragraph_type(ParagraphType.PROSE)
        .with_language_variant("Sanskrit")
        .as_translation()
        .as_commentary()
        .build()
    )

    rebuilt = ParagraphBuilder.from_paragraph(paragraph).build()

    assert rebuilt.metadata.paragraph_number == 5
    assert rebuilt.metadata.paragraph_type == ParagraphType.PROSE
    assert rebuilt.metadata.language_variant == "Sanskrit"
    assert rebuilt.metadata.is_translation is True
    assert rebuilt.metadata.is_commentary is True


def test_from_paragraph_copies_children():
    line = make_line()

    paragraph = (
        ParagraphBuilder()
        .add_line(line)
        .build()
    )

    rebuilt = ParagraphBuilder.from_paragraph(paragraph).build()

    assert rebuilt.child_count == 1
    assert rebuilt.first_child is line


def test_from_paragraph_does_not_alias_original():
    paragraph = (
        ParagraphBuilder()
        .with_language_variant("Sanskrit")
        .build()
    )

    rebuilt = ParagraphBuilder.from_paragraph(paragraph).build()

    rebuilt.metadata.language_variant = "Telugu"

    assert paragraph.metadata.language_variant == "Sanskrit"

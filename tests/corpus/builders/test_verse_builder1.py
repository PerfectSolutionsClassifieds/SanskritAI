
from SanskritAI.corpus.builders.verse_builder import VerseBuilder
from SanskritAI.corpus.builders.paragraph_builder import ParagraphBuilder
from SanskritAI.corpus.enums.meter import Meter
from SanskritAI.corpus.enums.verse_type import VerseType
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata


def make_paragraph(number: int = 1):
    return (
        ParagraphBuilder()
        .with_paragraph_number(number)
        .build()
    )


def test_create_instance_returns_verse():
    verse = VerseBuilder().build()

    assert isinstance(verse, Verse)


def test_create_instance_initializes_metadata():
    verse = VerseBuilder().build()

    assert isinstance(verse.metadata, VerseMetadata)


def test_create_instance_generates_identifier():
    first = VerseBuilder().build()
    second = VerseBuilder().build()

    assert first.identifier is not None
    assert second.identifier is not None
    assert first.identifier != second.identifier


def test_with_verse_number_is_fluent():
    builder = VerseBuilder()

    result = builder.with_verse_number("1")

    assert result is builder


def test_with_verse_type_is_fluent():
    builder = VerseBuilder()

    result = builder.with_verse_type(VerseType.SLOKA)

    assert result is builder


def test_with_meter_is_fluent():
    builder = VerseBuilder()

    result = builder.with_meter(Meter.ANUSTUBH)

    assert result is builder


def test_with_meter_name_is_fluent():
    builder = VerseBuilder()

    result = builder.with_meter_name("Anustubh")

    assert result is builder


def test_with_verse_number_sets_metadata():
    verse = (
        VerseBuilder()
        .with_verse_number("12")
        .build()
    )

    assert verse.metadata.verse_number == "12"


def test_with_verse_type_sets_metadata():
    verse = (
        VerseBuilder()
        .with_verse_type(VerseType.SLOKA)
        .build()
    )

    assert verse.metadata.verse_type == VerseType.SLOKA


def test_with_meter_sets_metadata():
    verse = (
        VerseBuilder()
        .with_meter(Meter.ANUSTUBH)
        .build()
    )

    assert verse.metadata.meter == Meter.ANUSTUBH


def test_with_meter_name_sets_metadata():
    verse = (
        VerseBuilder()
        .with_meter_name("Anustubh")
        .build()
    )

    assert verse.metadata.meter_name == "Anustubh"


def test_add_paragraph_is_fluent():
    paragraph = make_paragraph()

    builder = VerseBuilder()

    result = builder.add_paragraph(paragraph)

    assert result is builder


def test_add_paragraph_adds_child():
    paragraph = make_paragraph()

    verse = (
        VerseBuilder()
        .add_paragraph(paragraph)
        .build()
    )

    assert verse.child_count == 1
    assert verse.first_child is paragraph


def test_add_paragraphs_adds_all_children():
    paragraphs = [
        make_paragraph(1),
        make_paragraph(2),
        make_paragraph(3),
    ]

    verse = (
        VerseBuilder()
        .add_paragraphs(paragraphs)
        .build()
    )

    assert verse.child_count == 3
    assert list(verse) == paragraphs


def test_add_paragraphs_accepts_iterable():
    paragraphs = (
        make_paragraph(1),
        make_paragraph(2),
    )

    verse = (
        VerseBuilder()
        .add_paragraphs(iter(paragraphs))
        .build()
    )

    assert verse.child_count == 2
    assert list(verse) == list(paragraphs)


def test_build_returns_independent_copy():
    builder = (
        VerseBuilder()
        .with_verse_number("1")
    )

    first = builder.build()

    first.metadata.verse_number = "changed"

    second = builder.build()

    assert second.metadata.verse_number == "1"


def test_reset_creates_fresh_verse():
    builder = (
        VerseBuilder()
        .with_verse_number("1")
    )

    first = builder.build()

    builder.reset()

    second = builder.build()

    assert second is not first
    assert second.metadata.verse_number != "1"


def test_reset_clears_children():
    paragraph = make_paragraph()

    builder = (
        VerseBuilder()
        .add_paragraph(paragraph)
    )

    builder.reset()

    verse = builder.build()

    assert verse.child_count == 0


def test_from_verse_returns_builder():
    verse = (
        VerseBuilder()
        .with_verse_number("10")
        .with_verse_type(VerseType.SLOKA)
        .with_meter(Meter.ANUSTUBH)
        .build()
    )

    builder = VerseBuilder.from_verse(verse)

    assert isinstance(builder, VerseBuilder)


def test_from_verse_copies_metadata():
    verse = (
        VerseBuilder()
        .with_verse_number("10")
        .with_verse_type(VerseType.SLOKA)
        .with_meter(Meter.ANUSTUBH)
        .with_meter_name("Anustubh")
        .build()
    )

    rebuilt = VerseBuilder.from_verse(verse).build()

    assert rebuilt.metadata.verse_number == "10"
    assert rebuilt.metadata.verse_type == VerseType.SLOKA
    assert rebuilt.metadata.meter == Meter.ANUSTUBH
    assert rebuilt.metadata.meter_name == "Anustubh"


def test_from_verse_copies_children():
    paragraph = make_paragraph()

    verse = (
        VerseBuilder()
        .add_paragraph(paragraph)
        .build()
    )

    rebuilt = VerseBuilder.from_verse(verse).build()

    assert rebuilt.child_count == 1
    assert rebuilt.first_child is paragraph


def test_from_verse_does_not_alias_original():
    verse = (
        VerseBuilder()
        .with_verse_number("10")
        .build()
    )

    rebuilt = VerseBuilder.from_verse(verse).build()

    rebuilt.metadata.verse_number = "20"

    assert verse.metadata.verse_number == "10"


from SanskritAI.corpus.builders.verse_builder import VerseBuilder
from SanskritAI.corpus.builders.paragraph_builder import ParagraphBuilder
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata
from SanskritAI.corpus.enums.verse_type import VerseType
from SanskritAI.corpus.enums.meter import Meter


def make_verse(number="1"):
    return (
        VerseBuilder()
        .with_verse_number(number)
        .build()
    )


def make_paragraph(number=1):
    return (
        ParagraphBuilder()
        .with_paragraph_number(number)
        .build()
    )


def first_enum_member(enum_class):
    return next(iter(enum_class))


def test_create_instance_returns_verse():
    verse = VerseBuilder().build()

    assert isinstance(verse, Verse)


def test_create_instance_initializes_metadata():
    verse = VerseBuilder().build()

    assert isinstance(verse.metadata, VerseMetadata)


def test_create_instance_generates_identifier():
    first = VerseBuilder().build()
    second = VerseBuilder().build()

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_verse_number_is_fluent():
    builder = VerseBuilder()

    result = builder.with_verse_number("12")

    assert result is builder


def test_with_verse_number_sets_metadata():
    verse = (
        VerseBuilder()
        .with_verse_number("12")
        .build()
    )

    assert verse.metadata.verse_number == "12"


def test_with_verse_type_is_fluent():
    builder = VerseBuilder()
    value = first_enum_member(VerseType)

    result = builder.with_verse_type(value)

    assert result is builder


def test_with_verse_type_sets_metadata():
    value = first_enum_member(VerseType)

    verse = (
        VerseBuilder()
        .with_verse_type(value)
        .build()
    )

    assert verse.metadata.verse_type == value


def test_with_meter_is_fluent():
    builder = VerseBuilder()
    value = first_enum_member(Meter)

    result = builder.with_meter(value)

    assert result is builder


def test_with_meter_sets_metadata():
    value = first_enum_member(Meter)

    verse = (
        VerseBuilder()
        .with_meter(value)
        .build()
    )

    assert verse.metadata.meter == value


def test_with_meter_name_is_fluent():
    builder = VerseBuilder()

    result = builder.with_meter_name("Anushtubh")

    assert result is builder


def test_with_meter_name_sets_metadata():
    verse = (
        VerseBuilder()
        .with_meter_name("Anushtubh")
        .build()
    )

    assert verse.metadata.meter_name == "Anushtubh"


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

    assert len(verse.paragraphs) == 1
    assert verse.paragraphs[0] == paragraph


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

    assert len(verse.paragraphs) == 3
    assert verse.paragraphs == paragraphs


def test_add_paragraphs_preserves_order():
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

    assert verse.paragraphs[0] == paragraphs[0]
    assert verse.paragraphs[1] == paragraphs[1]
    assert verse.paragraphs[2] == paragraphs[2]


def test_build_returns_independent_copy():
    builder = VerseBuilder().with_verse_number("1")

    first = builder.build()

    builder.with_verse_number("2")

    second = builder.build()

    assert first.metadata.verse_number == "1"
    assert second.metadata.verse_number == "2"


def test_reset_creates_fresh_verse():
    builder = VerseBuilder().with_verse_number("1")

    original_id = builder.build().id

    builder.reset()

    fresh = builder.build()

    assert isinstance(fresh, Verse)
    assert fresh.id != original_id
    assert fresh.metadata.verse_number is None


def test_reset_clears_paragraphs():
    paragraph = make_paragraph()

    builder = VerseBuilder().add_paragraph(paragraph)

    assert len(builder.instance().paragraphs) == 1

    builder.reset()

    assert len(builder.instance().paragraphs) == 0


def test_from_verse_returns_verse_builder():
    verse = make_verse("5")

    builder = VerseBuilder.from_verse(verse)

    assert isinstance(builder, VerseBuilder)


def test_from_verse_copies_metadata():
    value = first_enum_member(VerseType)

    verse = (
        VerseBuilder()
        .with_verse_number("5")
        .with_verse_type(value)
        .with_meter_name("Anushtubh")
        .build()
    )

    copied = VerseBuilder.from_verse(verse).build()

    assert copied.metadata.verse_number == "5"
    assert copied.metadata.verse_type == value
    assert copied.metadata.meter_name == "Anushtubh"


def test_from_verse_does_not_alias_original():
    verse = (
        VerseBuilder()
        .with_verse_number("1")
        .build()
    )

    copied = VerseBuilder.from_verse(verse).build()

    copied.metadata.verse_number = "2"

    assert verse.metadata.verse_number == "1"
    assert copied.metadata.verse_number == "2"

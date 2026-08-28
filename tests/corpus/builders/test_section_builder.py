
from SanskritAI.corpus.builders.section_builder import SectionBuilder
from SanskritAI.corpus.builders.verse_builder import VerseBuilder
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata


def make_verse(number="1"):
    return (
        VerseBuilder()
        .with_title(f"Verse {number}")
        .with_verse_number(number)
        .build()
    )


def make_section(title="Adi Parva"):
    return (
        SectionBuilder()
        .with_title(title)
        .build()
    )


def test_create_instance_returns_section():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .build()
    )

    assert isinstance(section, Section)


def test_create_instance_initializes_metadata():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .build()
    )

    assert isinstance(section.metadata, SectionMetadata)


def test_create_instance_generates_identifier():
    first = (
        SectionBuilder()
        .with_title("First")
        .build()
    )

    second = (
        SectionBuilder()
        .with_title("Second")
        .build()
    )

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_title_is_fluent():
    builder = SectionBuilder()

    result = builder.with_title("Adi Parva")

    assert result is builder


def test_with_title_sets_metadata():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .build()
    )

    assert section.metadata.title == "Adi Parva"


def test_with_section_type_is_fluent():
    builder = (
        SectionBuilder()
        .with_title("Adi Parva")
    )

    result = builder.with_section_type("Parva")

    assert result is builder


def test_with_section_type_sets_metadata():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .with_section_type("Kanda")
        .build()
    )

    assert section.metadata.section_type == "Kanda"


def test_with_section_number_is_fluent():
    builder = (
        SectionBuilder()
        .with_title("Chapter")
    )

    result = builder.with_section_number("12")

    assert result is builder


def test_with_section_number_maps_to_numbering_scheme():
    section = (
        SectionBuilder()
        .with_title("Chapter")
        .with_section_number("12")
        .build()
    )

    assert section.metadata.numbering_scheme == "12"


def test_add_verse_is_fluent():
    verse = make_verse()

    builder = (
        SectionBuilder()
        .with_title("Adi Parva")
    )

    result = builder.add_verse(verse)

    assert result is builder


def test_add_verse_adds_verse():
    verse = make_verse()

    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .add_verse(verse)
        .build()
    )

    assert section.verse_count == 1
    assert section.first_verse == verse


def test_add_verses_adds_all_verses():
    verses = [
        make_verse("1"),
        make_verse("2"),
        make_verse("3"),
    ]

    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .add_verses(verses)
        .build()
    )

    assert section.verse_count == 3


def test_add_verses_preserves_order():
    verses = [
        make_verse("1"),
        make_verse("2"),
        make_verse("3"),
    ]

    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .add_verses(verses)
        .build()
    )

    assert list(section.verses) == verses


def test_build_returns_section():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .with_section_type("Parva")
        .with_section_number("1")
        .build()
    )

    assert isinstance(section, Section)
    assert section.metadata.title == "Adi Parva"
    assert section.metadata.section_type == "Parva"


def test_build_returns_independent_copy():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    first = builder.build()

    builder.with_title("Modified")

    second = builder.build()

    assert first.metadata.title == "Original"
    assert second.metadata.title == "Modified"
    assert first is not second


def test_reset_creates_fresh_section():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    original = builder.build()

    builder.reset()

    fresh = (
        builder
        .with_title("Fresh")
        .build()
    )

    assert fresh.metadata.title == "Fresh"
    assert fresh.id != original.id


def test_reset_clears_verses():
    verse = make_verse()

    builder = (
        SectionBuilder()
        .with_title("Adi Parva")
        .add_verse(verse)
    )

    before_reset = builder.build()

    builder.reset()

    after_reset = (
        builder
        .with_title("Fresh Section")
        .build()
    )

    assert before_reset.verse_count == 1
    assert after_reset.verse_count == 0


def test_from_section_returns_section_builder():
    section = make_section()

    builder = SectionBuilder.from_section(section)

    assert isinstance(builder, SectionBuilder)


def test_from_section_copies_metadata():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .with_section_type("Parva")
        .with_section_number("1")
        .build()
    )

    copied = SectionBuilder.from_section(section).build()

    assert copied.metadata.title == section.metadata.title
    assert copied.metadata.section_type == section.metadata.section_type
    assert copied.metadata.numbering_scheme == (
        section.metadata.numbering_scheme
    )


def test_from_section_does_not_alias_original():
    section = (
        SectionBuilder()
        .with_title("Original")
        .build()
    )

    builder = SectionBuilder.from_section(section)

    builder.with_title("Modified")

    assert section.metadata.title == "Original"
    assert builder.build().metadata.title == "Modified"

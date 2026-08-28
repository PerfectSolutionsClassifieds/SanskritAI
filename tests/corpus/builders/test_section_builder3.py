
from SanskritAI.corpus.builders.section_builder import SectionBuilder
from SanskritAI.corpus.builders.verse_builder import VerseBuilder
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.verse import Verse


def make_section(title: str = "Section") -> Section:
    return (
        SectionBuilder()
        .with_title(title)
        .build()
    )


def make_verse(number: str = "1") -> Verse:
    return (
        VerseBuilder()
        .with_verse_number(number)
        .build()
    )


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def test_create_instance_returns_section():
    section = SectionBuilder().build()

    assert isinstance(section, Section)


def test_create_instance_initializes_metadata():
    section = SectionBuilder().build()

    assert section.metadata is not None


def test_create_instance_generates_identifier():
    first = SectionBuilder().build()
    second = SectionBuilder().build()

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


# ---------------------------------------------------------------------------
# Common metadata
# ---------------------------------------------------------------------------

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
    builder = SectionBuilder()

    result = builder.with_section_type("Kanda")

    assert result is builder


def test_with_section_type_sets_metadata():
    section = (
        SectionBuilder()
        .with_section_type("Kanda")
        .build()
    )

    assert section.metadata.section_type == "Kanda"


def test_with_section_number_is_fluent():
    builder = SectionBuilder()

    result = builder.with_section_number("12")

    assert result is builder


def test_with_section_number_sets_metadata():
    section = (
        SectionBuilder()
        .with_section_number("12")
        .build()
    )

    assert section.metadata.section_number == "12"


# ---------------------------------------------------------------------------
# Verse hierarchy
# ---------------------------------------------------------------------------

def test_add_verse_is_fluent():
    verse = make_verse()

    builder = SectionBuilder()

    result = builder.add_verse(verse)

    assert result is builder


def test_add_verse_adds_child():
    verse = make_verse()

    section = (
        SectionBuilder()
        .add_verse(verse)
        .build()
    )

    assert section.verse_count == 1
    assert section.first_verse == verse


def test_add_verses_adds_all_children():
    verses = [
        make_verse("1"),
        make_verse("2"),
        make_verse("3"),
    ]

    section = (
        SectionBuilder()
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
        .add_verses(verses)
        .build()
    )

    assert list(section.verses) == verses


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

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
    assert section.metadata.section_number == "1"


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


# ---------------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------------

def test_reset_creates_fresh_section():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    original = builder.build()

    result = builder.reset()
    reset_section = builder.build()

    assert result is builder
    assert reset_section.id != original.id
    assert reset_section.metadata.title == ""


def test_reset_clears_children():
    verse = make_verse()

    builder = (
        SectionBuilder()
        .add_verse(verse)
    )

    assert builder.build().verse_count == 1

    builder.reset()

    section = builder.build()

    assert section.verse_count == 0


# ---------------------------------------------------------------------------
# from_section
# ---------------------------------------------------------------------------

def test_from_section_returns_section_builder():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .with_section_type("Parva")
        .build()
    )

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

    assert copied.metadata.title == "Adi Parva"
    assert copied.metadata.section_type == "Parva"
    assert copied.metadata.section_number == "1"


def test_from_section_does_not_alias_original():
    section = (
        SectionBuilder()
        .with_title("Original")
        .build()
    )

    copied = (
        SectionBuilder
        .from_section(section)
        .with_title("Copied")
        .build()
    )

    assert section.metadata.title == "Original"
    assert copied.metadata.title == "Copied"

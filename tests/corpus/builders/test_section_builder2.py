
from SanskritAI.corpus.builders.section_builder import SectionBuilder
from SanskritAI.corpus.builders.verse_builder import VerseBuilder
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse import Verse


def make_section(title="Child Section"):
    return (
        SectionBuilder()
        .with_title(title)
        .with_section_type("Parva")
        .with_section_number("1")
        .build()
    )


def make_verse(number="1"):
    return (
        VerseBuilder()
        .with_verse_number(number)
        .build()
    )


def test_create_instance_returns_section():
    builder = SectionBuilder()

    section = builder.build()

    assert isinstance(section, Section)


def test_create_instance_initializes_metadata():
    section = SectionBuilder().build()

    assert isinstance(section.metadata, SectionMetadata)


def test_create_instance_generates_identifier():
    first = SectionBuilder().build()
    second = SectionBuilder().build()

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_section_type_is_fluent():
    builder = SectionBuilder()

    result = builder.with_section_type("Kanda")

    assert result is builder


def test_with_section_number_is_fluent():
    builder = SectionBuilder()

    result = builder.with_section_number("12")

    assert result is builder


def test_with_section_type_sets_metadata():
    section = (
        SectionBuilder()
        .with_section_type("Kanda")
        .build()
    )

    assert section.metadata.section_type == "Kanda"


def test_with_section_number_sets_metadata():
    section = (
        SectionBuilder()
        .with_section_number("12")
        .build()
    )

    assert section.metadata.section_number == "12"


def test_add_section_is_fluent():
    child = make_section()

    builder = SectionBuilder()

    result = builder.add_section(child)

    assert result is builder


def test_add_section_adds_child():
    child = make_section()

    section = (
        SectionBuilder()
        .add_section(child)
        .build()
    )

    assert len(section.children) == 1
    assert section.children[0] == child


def test_add_sections_adds_all_children():
    children = [
        make_section("Section 1"),
        make_section("Section 2"),
        make_section("Section 3"),
    ]

    section = (
        SectionBuilder()
        .add_sections(children)
        .build()
    )

    assert len(section.children) == 3
    assert section.children == children


def test_add_sections_preserves_order():
    children = [
        make_section("First"),
        make_section("Second"),
        make_section("Third"),
    ]

    section = (
        SectionBuilder()
        .add_sections(children)
        .build()
    )

    assert section.children[0] == children[0]
    assert section.children[1] == children[1]
    assert section.children[2] == children[2]


def test_add_verse_is_fluent():
    verse = make_verse()

    builder = SectionBuilder()

    result = builder.add_verse(verse)

    assert result is builder


def test_add_verse_adds_verse():
    verse = make_verse()

    section = (
        SectionBuilder()
        .add_verse(verse)
        .build()
    )

    assert len(section.verses) == 1
    assert section.verses[0] == verse


def test_add_verses_adds_all_verses():
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

    assert len(section.verses) == 3
    assert section.verses == verses


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

    assert section.verses[0] == verses[0]
    assert section.verses[1] == verses[1]
    assert section.verses[2] == verses[2]


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


def test_build_returns_independent_copy():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    first = builder.build()

    builder.with_title("Changed")

    second = builder.build()

    assert first.metadata.title == "Original"
    assert second.metadata.title == "Changed"


def test_reset_creates_fresh_section():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    original_id = builder.build().id

    builder.reset()

    fresh = builder.build()

    assert isinstance(fresh, Section)
    assert fresh.id != original_id
    assert fresh.metadata.title is None


def test_reset_clears_children():
    child = make_section()

    builder = (
        SectionBuilder()
        .add_section(child)
    )

    assert len(builder.instance().children) == 1

    builder.reset()

    assert len(builder.instance().children) == 0


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

    copied = SectionBuilder.from_section(section).build()

    copied.metadata.title = "Changed"

    assert section.metadata.title == "Original"
    assert copied.metadata.title == "Changed"

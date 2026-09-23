
from SanskritAI.corpus.builders.section_builder import SectionBuilder
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata


def make_section(title: str = "Child Section") -> Section:
    return (
        SectionBuilder()
        .with_title(title)
        .build()
    )


def make_verse(number: str = "1") :
    from SanskritAI.corpus.builders.verse_builder import VerseBuilder

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
    builder = SectionBuilder()

    section = builder.build()

    assert isinstance(section.metadata, SectionMetadata)


def test_create_instance_generates_identifier():
    first = SectionBuilder().build()
    second = SectionBuilder().build()

    assert first.identifier is not None
    assert second.identifier is not None
    assert first.identifier != second.identifier


def test_with_section_type_is_fluent():
    builder = SectionBuilder()

    result = builder.with_section_type("Kanda")

    assert result is builder


def test_with_section_number_is_fluent():
    builder = SectionBuilder()

    result = builder.with_section_number("01")

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

    assert section.child_count == 1
    assert section.first_child is child


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

    assert section.child_count == 3
    assert list(section) == children


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

    assert section[0] is children[0]
    assert section[1] is children[1]
    assert section[2] is children[2]


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

    assert section.child_count == 1
    assert section.first_child is verse


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

    assert section.child_count == 3
    assert list(section) == verses


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

    assert section[0] is verses[0]
    assert section[1] is verses[1]
    assert section[2] is verses[2]


def test_build_returns_section():
    section = (
        SectionBuilder()
        .with_title("Adi Parva")
        .with_section_type("Parva")
        .with_section_number("1")
        .build()
    )

    assert isinstance(section, Section)


def test_build_returns_independent_copy():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    first = builder.build()

    first.metadata.title = "Changed"

    second = builder.build()

    assert second.metadata.title == "Original"


def test_reset_creates_fresh_section():
    builder = (
        SectionBuilder()
        .with_title("Original")
    )

    first = builder.build()

    result = builder.reset()

    assert result is builder

    second = builder.build()

    assert second is not first
    assert second.metadata.title != "Original"


def test_reset_clears_children():
    child = make_section()

    builder = (
        SectionBuilder()
        .add_section(child)
    )

    builder.reset()

    section = builder.build()

    assert section.child_count == 0


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

    rebuilt = SectionBuilder.from_section(section).build()

    assert rebuilt.metadata.title == "Adi Parva"
    assert rebuilt.metadata.section_type == "Parva"
    assert rebuilt.metadata.section_number == "1"


def test_from_section_does_not_alias_original():
    section = (
        SectionBuilder()
        .with_title("Original")
        .build()
    )

    rebuilt = SectionBuilder.from_section(section).build()

    rebuilt.metadata.title = "Changed"

    assert section.metadata.title == "Original"

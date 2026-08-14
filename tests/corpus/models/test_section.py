
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata


def make_section(identifier="section-1"):
    return Section(
        identifier=identifier,
        metadata=SectionMetadata(),
    )


def make_verse(identifier="verse-1"):
    return Verse(
        identifier=identifier,
        metadata=VerseMetadata(),
    )


def test_section_stores_identifier():
    section = make_section()

    assert section.id == "section-1"


def test_section_stores_metadata():
    metadata = SectionMetadata()

    section = Section(
        identifier="section-1",
        metadata=metadata,
    )

    assert section.metadata is metadata


def test_section_starts_without_verses():
    section = make_section()

    assert section.verses == []
    assert section.verse_count == 0


def test_verses_alias_children():
    section = make_section()

    assert section.verses is section.children


def test_add_verse():
    section = make_section()
    verse = make_verse()

    section.add_verse(verse)

    assert section.verses == [verse]
    assert section.verse_count == 1


def test_remove_verse():
    section = make_section()
    verse = make_verse()

    section.add_verse(verse)
    section.remove_verse(verse)

    assert section.verses == []
    assert section.verse_count == 0


def test_first_verse():
    section = make_section()
    first = make_verse("verse-1")
    second = make_verse("verse-2")

    section.add_verse(first)
    section.add_verse(second)

    assert section.first_verse is first


def test_last_verse():
    section = make_section()
    first = make_verse("verse-1")
    second = make_verse("verse-2")

    section.add_verse(first)
    section.add_verse(second)

    assert section.last_verse is second


def test_verses_preserve_insertion_order():
    section = make_section()

    verses = [
        make_verse("verse-1"),
        make_verse("verse-2"),
        make_verse("verse-3"),
    ]

    for verse in verses:
        section.add_verse(verse)

    assert section.verses == verses

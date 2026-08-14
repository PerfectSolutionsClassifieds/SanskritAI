
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata


def make_verse(identifier="verse-1"):
    return Verse(
        identifier=identifier,
        metadata=VerseMetadata(),
    )


def make_paragraph(identifier="paragraph-1"):
    return Paragraph(
        identifier=identifier,
        metadata=ParagraphMetadata(),
    )


def test_verse_stores_identifier():
    verse = make_verse()

    assert verse.id == "verse-1"


def test_verse_stores_metadata():
    metadata = VerseMetadata()

    verse = Verse(
        identifier="verse-1",
        metadata=metadata,
    )

    assert verse.metadata is metadata


def test_verse_starts_without_paragraphs():
    verse = make_verse()

    assert verse.paragraphs == []
    assert verse.paragraph_count == 0


def test_paragraphs_alias_children():
    verse = make_verse()

    assert verse.paragraphs is verse.children


def test_add_paragraph():
    verse = make_verse()
    paragraph = make_paragraph()

    verse.add_paragraph(paragraph)

    assert verse.paragraphs == [paragraph]
    assert verse.paragraph_count == 1


def test_remove_paragraph():
    verse = make_verse()
    paragraph = make_paragraph()

    verse.add_paragraph(paragraph)
    verse.remove_paragraph(paragraph)

    assert verse.paragraphs == []
    assert verse.paragraph_count == 0


def test_first_paragraph():
    verse = make_verse()

    first = make_paragraph("paragraph-1")
    second = make_paragraph("paragraph-2")

    verse.add_paragraph(first)
    verse.add_paragraph(second)

    assert verse.first_paragraph is first


def test_last_paragraph():
    verse = make_verse()

    first = make_paragraph("paragraph-1")
    second = make_paragraph("paragraph-2")

    verse.add_paragraph(first)
    verse.add_paragraph(second)

    assert verse.last_paragraph is second


def test_paragraphs_preserve_insertion_order():
    verse = make_verse()

    paragraphs = [
        make_paragraph("paragraph-1"),
        make_paragraph("paragraph-2"),
        make_paragraph("paragraph-3"),
    ]

    for paragraph in paragraphs:
        verse.add_paragraph(paragraph)

    assert verse.paragraphs == paragraphs

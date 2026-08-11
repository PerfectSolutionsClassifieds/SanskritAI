from __future__ import annotations

"""
SanskritAI
==========

Corpus Navigation Structure Tests

Verifies the canonical structural hierarchy:

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token
"""

from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.token import Token

from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse_metadata import VerseMetadata
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata
from SanskritAI.corpus.models.line_metadata import LineMetadata
from SanskritAI.corpus.models.token_metadata import TokenMetadata


def test_canonical_corpus_hierarchy_navigation():
    """
    Verify that the canonical Corpus hierarchy can be traversed
    from the root down to individual Tokens.
    """

    token = Token(
        identifier="word-1",
        metadata=TokenMetadata(
            text="धर्मः",
            normalized_text="धर्मः",
        ),
    )

    line = Line(
        identifier="line-1",
        metadata=LineMetadata(),
    )

    line.add_token(token)

    paragraph = Paragraph(
        identifier="paragraph-1",
        metadata=ParagraphMetadata(),
    )

    paragraph.add_line(line)

    verse = Verse(
        identifier="sloka-1",
        metadata=VerseMetadata(),
    )

    verse.add_paragraph(paragraph)

    section = Section(
        identifier="chapter-1",
        metadata=SectionMetadata(),
    )

    section.add_verse(verse)

    document = Document(
        identifier="document-1",
        metadata=DocumentMetadata(),
    )

    document.add_section(section)

    corpus = Corpus(
        id="corpus-1",
        metadata=CorpusMetadata(),
    )

    corpus.add_document(document)

    # ---------------------------------------------------------
    # Root
    # ---------------------------------------------------------

    assert corpus.document_count == 1
    assert corpus[0] is document

    # ---------------------------------------------------------
    # Document
    # ---------------------------------------------------------

    assert document.section_count == 1
    assert document.first_section is section

    # ---------------------------------------------------------
    # Section
    # ---------------------------------------------------------

    assert section.verse_count == 1
    assert section.first_verse is verse

    # ---------------------------------------------------------
    # Verse
    # ---------------------------------------------------------

    assert verse.paragraph_count == 1
    assert verse.first_paragraph is paragraph

    # ---------------------------------------------------------
    # Paragraph
    # ---------------------------------------------------------

    assert paragraph.line_count == 1
    assert paragraph.first_line is line

    # ---------------------------------------------------------
    # Line
    # ---------------------------------------------------------

    assert line.token_count == 1
    assert line.first_token is token

    # ---------------------------------------------------------
    # Token
    # ---------------------------------------------------------

    assert token.identifier == "word-1"
    assert token.text == "धर्मः"


def test_canonical_order_is_preserved():
    """
    Verify that insertion order is preserved at every container
    level.
    """

    corpus = Corpus(
        id="corpus-1",
        metadata=CorpusMetadata(),
    )

    document = Document(
        identifier="document-1",
        metadata=DocumentMetadata(),
    )

    section_1 = Section(
        identifier="chapter-1",
        metadata=SectionMetadata(),
    )

    section_2 = Section(
        identifier="chapter-2",
        metadata=SectionMetadata(),
    )

    document.add_section(section_1)
    document.add_section(section_2)

    corpus.add_document(document)

    assert document.sections[0].identifier == "chapter-1"
    assert document.sections[1].identifier == "chapter-2"

    assert list(document)[0] is section_1
    assert list(document)[1] is section_2

from __future__ import annotations

"""
SanskritAI
==========

ReaderSession Integration Tests

Verifies the complete Reader Domain stack:

    Corpus
        ↓
    DefaultReaderRepository
        ↓
    ReaderNavigator
        ↓
    ReaderEngine
        ↓
    ReaderSession

These tests intentionally use the real implementations rather
than mocks.

The purpose is to verify that ReaderSession correctly operates
over the canonical Corpus hierarchy.

Canonical hierarchy
-------------------

Corpus
    └── Document
          ├── Section / Chapter
          │     ├── Verse / Śloka
          │     │     └── Paragraph
          │     │           └── Line
          │     │                 └── Token / Word
          │     └── ...
          └── ...

ReaderPosition
--------------

purana_id
chapter_id
sloka_id
word_id

Version
-------
v1.0.0
"""

import pytest

from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.token import Token

from SanskritAI.corpus.models.corpus_metadata import (
    CorpusMetadata,
)

from SanskritAI.corpus.models.document_metadata import (
    DocumentMetadata,
)

from SanskritAI.corpus.models.section_metadata import (
    SectionMetadata,
)

from SanskritAI.corpus.models.verse_metadata import (
    VerseMetadata,
)

from SanskritAI.corpus.models.paragraph_metadata import (
    ParagraphMetadata,
)

from SanskritAI.corpus.models.line_metadata import (
    LineMetadata,
)

from SanskritAI.corpus.models.token_metadata import (
    TokenMetadata,
)

from SanskritAI.domain.reader.default_reader_repository import (
    DefaultReaderRepository,
)

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)

from SanskritAI.domain.reader.reader_navigator import (
    ReaderNavigator,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_session import (
    ReaderSession,
)


# =============================================================
# Corpus Construction Helpers
# =============================================================


def _token(
    identifier: str,
    text: str,
    position: int,
) -> Token:

    return Token(
        identifier=identifier,
        metadata=TokenMetadata(
            identifier=identifier,
            token_index=position,
            normalized_text=text,
        ),
    )


def _line(
    identifier: str,
    *tokens: Token,
) -> Line:

    line = Line(
        identifier=identifier,
        metadata=LineMetadata(),
    )

    for token in tokens:
        line.add_token(token)

    return line


def _paragraph(
    identifier: str,
    *lines: Line,
) -> Paragraph:

    paragraph = Paragraph(
        identifier=identifier,
        metadata=ParagraphMetadata(),
    )

    for line in lines:
        paragraph.add_line(line)

    return paragraph


def _verse(
    identifier: str,
    *paragraphs: Paragraph,
) -> Verse:

    verse = Verse(
        identifier=identifier,
        metadata=VerseMetadata(),
    )

    for paragraph in paragraphs:
        verse.add_paragraph(paragraph)

    return verse


def _section(
    identifier: str,
    *verses: Verse,
) -> Section:

    section = Section(
        identifier=identifier,
        metadata=SectionMetadata(),
    )

    for verse in verses:
        section.add_verse(verse)

    return section


def _document(
    identifier: str,
    *sections: Section,
) -> Document:

    document = Document(
        identifier=identifier,
        metadata=DocumentMetadata(
            title=identifier,
        ),
    )

    for section in sections:
        document.add_section(section)

    return document


# =============================================================
# Corpus Fixture
# =============================================================


@pytest.fixture
def corpus() -> Corpus:
    """
    Build a small but complete canonical Corpus.

    Structure:

        Corpus
          └── Document
                ├── Chapter 1
                │     ├── Śloka 1
                │     │     └── word-1, word-2
                │     └── Śloka 2
                │           └── word-3, word-4
                │
                └── Chapter 2
                      └── Śloka 3
                            └── word-5, word-6
    """

    sloka_1 = _verse(
        "sloka-1",
        _paragraph(
            "paragraph-1",
            _line(
                "line-1",
                _token(
                    "word-1",
                    "धर्मः",
                    1,
                ),
                _token(
                    "word-2",
                    "रक्षति",
                    2,
                ),
            ),
        ),
    )

    sloka_2 = _verse(
        "sloka-2",
        _paragraph(
            "paragraph-2",
            _line(
                "line-2",
                _token(
                    "word-3",
                    "धर्मः",
                    1,
                ),
                _token(
                    "word-4",
                    "सर्वदा",
                    2,
                ),
            ),
        ),
    )

    sloka_3 = _verse(
        "sloka-3",
        _paragraph(
            "paragraph-3",
            _line(
                "line-3",
                _token(
                    "word-5",
                    "सत्यं",
                    1,
                ),
                _token(
                    "word-6",
                    "वद",
                    2,
                ),
            ),
        ),
    )

    chapter_1 = _section(
        "chapter-1",
        sloka_1,
        sloka_2,
    )

    chapter_2 = _section(
        "chapter-2",
        sloka_3,
    )

    document = _document(
        "document-1",
        chapter_1,
        chapter_2,
    )

    corpus = Corpus(
        id="corpus-1",
        metadata=CorpusMetadata(
            title="Test Purāṇa",
        ),
    )

    corpus.add_document(
        document,
    )

    return corpus


# =============================================================
# Real Reader Stack
# =============================================================


@pytest.fixture
def repository(
    corpus,
) -> DefaultReaderRepository:

    return DefaultReaderRepository(
        corpus=corpus,
    )


@pytest.fixture
def navigator(
    repository,
) -> ReaderNavigator:

    return ReaderNavigator(
        repository=repository,
    )


@pytest.fixture
def engine(
    repository,
    navigator,
) -> ReaderEngine:

    return ReaderEngine(
        repository=repository,
        navigator=navigator,
    )


# =============================================================
# Session Opening
# =============================================================


def test_session_opens_at_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session = ReaderSession.open(
        engine=engine,
        position=position,
    )

    assert session.position == position
    assert session.result is not None
    assert session.result.identifier == "chapter-1"


def test_session_opens_at_sloka(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    session = ReaderSession.open(
        engine=engine,
        position=position,
    )

    assert session.position == position
    assert session.result is not None
    assert session.result.identifier == "sloka-1"


def test_session_opens_at_word(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    session = ReaderSession.open(
        engine=engine,
        position=position,
    )

    assert session.position == position
    assert session.result is not None
    assert session.result.identifier == "word-1"


# =============================================================
# Chapter Navigation
# =============================================================


def test_session_moves_to_next_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    next_session = session.move_next()

    assert next_session is not None

    assert (
        next_session.position.chapter_id
        == "chapter-2"
    )

    assert (
        next_session.result.identifier
        == "chapter-2"
    )


def test_session_moves_to_previous_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    previous_session = (
        session.move_previous()
    )

    assert previous_session is not None

    assert (
        previous_session.position.chapter_id
        == "chapter-1"
    )

    assert (
        previous_session.result.identifier
        == "chapter-1"
    )


# =============================================================
# Śloka Navigation
# =============================================================


def test_session_moves_to_next_sloka(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    next_session = session.move_next()

    assert next_session is not None

    assert (
        next_session.position.sloka_id
        == "sloka-2"
    )

    assert (
        next_session.result.identifier
        == "sloka-2"
    )


def test_session_moves_to_previous_sloka(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-2",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    previous_session = (
        session.move_previous()
    )

    assert previous_session is not None

    assert (
        previous_session.position.sloka_id
        == "sloka-1"
    )

    assert (
        previous_session.result.identifier
        == "sloka-1"
    )


# =============================================================
# Word Navigation
# =============================================================


def test_session_moves_to_next_word(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    next_session = session.move_next()

    assert next_session is not None

    assert (
        next_session.position.word_id
        == "word-2"
    )

    assert (
        next_session.result.identifier
        == "word-2"
    )


def test_session_moves_to_previous_word(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    previous_session = (
        session.move_previous()
    )

    assert previous_session is not None

    assert (
        previous_session.position.word_id
        == "word-1"
    )

    assert (
        previous_session.result.identifier
        == "word-1"
    )


# =============================================================
# Navigation Boundaries
# =============================================================


def test_session_returns_none_after_last_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.move_next()
        is None
    )


def test_session_returns_none_before_first_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.move_previous()
        is None
    )


# =============================================================
# Session Immutability
# =============================================================


def test_navigation_does_not_mutate_original_session(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    next_session = session.move_next()

    assert next_session is not None
    assert next_session is not session

    assert (
        session.position.chapter_id
        == "chapter-1"
    )

    assert (
        next_session.position.chapter_id
        == "chapter-2"
    )


# =============================================================
# Corpus Hierarchy → ReaderSession
# =============================================================


def test_session_result_preserves_chapter_sloka_hierarchy(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    result = session.result

    assert result.identifier == "sloka-1"

    assert result.position.purana_id == "corpus-1"
    assert result.position.chapter_id == "chapter-1"
    assert result.position.sloka_id == "sloka-1"


# =============================================================
# Re-resolution
# =============================================================


def test_session_resolve_reloads_current_position(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    refreshed = session.resolve()

    assert refreshed is not session

    assert (
        refreshed.position
        == session.position
    )

    assert (
        refreshed.result.identifier
        == "sloka-1"
    )

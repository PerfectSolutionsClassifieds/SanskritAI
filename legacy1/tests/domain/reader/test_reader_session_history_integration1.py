
from __future__ import annotations

"""
SanskritAI
==========

ReaderSessionHistory Integration Tests

Verifies the integration between:

    Corpus
        ↓
    DefaultReaderRepository
        ↓
    ReaderNavigator
        ↓
    ReaderEngine
        ↓
    ReaderSession
        ↓
    ReaderSessionHistory

The tests use the real Reader domain components.

The purpose is to verify that ReaderSession correctly owns and
uses ReaderSessionHistory while navigation remains identifier-based.

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

from SanskritAI.domain.reader.reader_session_history import (
    ReaderSessionHistory,
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
    Build a minimal real Corpus.

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
# Integrated Reader Fixtures
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


@pytest.fixture
def history() -> ReaderSessionHistory:

    return ReaderSessionHistory()


@pytest.fixture
def session(
    engine,
    history,
) -> ReaderSession:

    return ReaderSession(
        engine=engine,
        history=history,
    )


# =============================================================
# Initial Session / History State
# =============================================================


def test_session_starts_with_empty_history(
    session,
):

    assert session.history is not None

    assert session.history.is_empty is True

    assert session.history.current is None

    assert session.history.back_count == 0
    assert session.history.forward_count == 0


# =============================================================
# Initial Position Recording
# =============================================================


def test_session_records_initial_position_in_history(
    session,
):

    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session.open(
        position,
    )

    assert session.current_position == position

    assert session.history.current == position

    assert session.history.history_count == 1

    assert session.history.can_go_back is False
    assert session.history.can_go_forward is False


# =============================================================
# Session Navigation → History
# =============================================================


def test_session_next_navigation_records_history(
    session,
):

    initial = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session.open(
        initial,
    )

    result = session.move_next()

    assert result is not None

    assert result.chapter_id == "chapter-2"

    assert session.current_position == result

    assert session.history.current == result

    assert session.history.back_count == 1
    assert session.history.forward_count == 0

    assert session.history.previous == initial


# =============================================================
# Back Navigation
# =============================================================


def test_session_back_uses_history(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    chapter_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session.open(
        chapter_1,
    )

    session.open(
        chapter_2,
    )

    result = session.back()

    assert result == chapter_1

    assert session.current_position == chapter_1

    assert session.history.current == chapter_1

    assert session.history.back_count == 0
    assert session.history.forward_count == 1

    assert session.history.next == chapter_2


# =============================================================
# Forward Navigation
# =============================================================


def test_session_forward_uses_history(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    chapter_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session.open(
        chapter_1,
    )

    session.open(
        chapter_2,
    )

    assert session.back() == chapter_1

    result = session.forward()

    assert result == chapter_2

    assert session.current_position == chapter_2

    assert session.history.current == chapter_2

    assert session.history.back_count == 1
    assert session.history.forward_count == 0


# =============================================================
# Back → Forward Round Trip
# =============================================================


def test_session_history_round_trip(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    chapter_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session.open(
        chapter_1,
    )

    session.open(
        chapter_2,
    )

    assert session.back() == chapter_1

    assert session.forward() == chapter_2

    assert session.current_position == chapter_2

    assert session.history.back_count == 1
    assert session.history.forward_count == 0


# =============================================================
# New Navigation Branch
# =============================================================


def test_new_session_position_clears_forward_history(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    chapter_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    chapter_3 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-3",
    )

    session.open(
        chapter_1,
    )

    session.open(
        chapter_2,
    )

    assert session.back() == chapter_1

    assert session.history.can_go_forward is True

    session.open(
        chapter_3,
    )

    assert session.current_position == chapter_3

    assert session.history.current == chapter_3

    assert session.history.can_go_forward is False

    assert session.history.forward_count == 0

    assert session.history.next is None


# =============================================================
# Boundary Behaviour
# =============================================================


def test_session_back_returns_none_at_first_position(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session.open(
        chapter_1,
    )

    assert session.back() is None

    assert session.current_position == chapter_1

    assert session.history.back_count == 0


def test_session_forward_returns_none_without_forward_history(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session.open(
        chapter_1,
    )

    assert session.forward() is None

    assert session.current_position == chapter_1

    assert session.history.forward_count == 0


# =============================================================
# Real Engine Navigation
# =============================================================


def test_session_uses_real_engine_for_navigation(
    session,
):

    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    session.open(
        position,
    )

    result = session.move_next()

    assert result is not None

    assert result.chapter_id == "chapter-2"

    assert session.current_position.chapter_id == (
        "chapter-2"
    )


# =============================================================
# Śloka-Level History
# =============================================================


def test_session_history_tracks_sloka_navigation(
    session,
):

    sloka_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    sloka_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-2",
    )

    session.open(
        sloka_1,
    )

    session.open(
        sloka_2,
    )

    assert session.current_position == sloka_2

    assert session.history.previous == sloka_1

    assert session.back() == sloka_1

    assert session.forward() == sloka_2


# =============================================================
# Word-Level History
# =============================================================


def test_session_history_tracks_word_navigation(
    session,
):

    word_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    word_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )

    session.open(
        word_1,
    )

    session.open(
        word_2,
    )

    assert session.current_position == word_2

    assert session.history.previous == word_1

    assert session.back() == word_1

    assert session.forward() == word_2


# =============================================================
# History Clear Through Session
# =============================================================


def test_session_can_clear_history(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    chapter_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session.open(
        chapter_1,
    )

    session.open(
        chapter_2,
    )

    session.clear_history()

    assert session.history.is_empty is True

    assert session.history.current is None
    assert session.history.back_count == 0
    assert session.history.forward_count == 0


# =============================================================
# Session / History Identity
# =============================================================


def test_session_uses_injected_history_instance(
    engine,
):

    history = ReaderSessionHistory()

    session = ReaderSession(
        engine=engine,
        history=history,
    )

    assert session.history is history


# =============================================================
# History Does Not Replace Engine Navigation
# =============================================================


def test_history_back_and_engine_navigation_remain_distinct(
    session,
):

    chapter_1 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    chapter_2 = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    session.open(
        chapter_1,
    )

    session.open(
        chapter_2,
    )

    # History navigation moves backward.

    assert session.back() == chapter_1

    # Forward history restores the previous session state.

    assert session.forward() == chapter_2

    # Engine navigation remains responsible for canonical
    # corpus navigation.

    assert session.back() == chapter_1

    result = session.move_next()

    assert result is not None
    assert result.chapter_id == "chapter-2"

    assert session.current_position == chapter_2

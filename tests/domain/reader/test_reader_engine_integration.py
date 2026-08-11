from __future__ import annotations

"""
SanskritAI
==========

Reader Engine Integration Tests

Verifies the integration boundary between:

    Corpus Domain
        ↓
    DefaultReaderRepository
        ↓
    ReaderNavigator
        ↓
    ReaderEngine

Unlike the unit tests for ReaderEngine, these tests intentionally
use the real ReaderRepository and ReaderNavigator implementations.

The purpose is to verify that the Reader Domain is correctly wired
to the canonical Corpus Domain.

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

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)
from SanskritAI.domain.reader.default_reader_repository import (
    DefaultReaderRepository,
)
from SanskritAI.domain.reader.reader_navigator import (
    ReaderNavigator,
)
from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


# =============================================================
# Corpus Fixture Helpers
# =============================================================


# def _token(
#     identifier: str,
#     text: str,
#     position: int,
# ) -> Token:

#     return Token(
#         identifier=identifier,
#         metadata=TokenMetadata(
#             text=text,
#             normalized_text=text,
#             position=position,
#         ),
#     )

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


@pytest.fixture
def corpus() -> Corpus:
    """
    Build a minimal canonical Corpus fixture.

    Structure:

        Corpus
          └── Document
                ├── Chapter 1
                │     ├── Śloka 1
                │     └── Śloka 2
                │
                └── Chapter 2
                      └── Śloka 3
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
# Integrated Reader Fixture
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
# Repository → Reader Projection
# =============================================================


def test_repository_projects_corpus_into_reader_document(
    repository,
):
    document = repository.get_document()

    assert document is repository.document

    assert repository.chapter_count == 2
    assert repository.sloka_count == 3
    assert repository.word_count == 6


# =============================================================
# Canonical ID Lookup
# =============================================================


def test_repository_resolves_chapter_by_canonical_id(
    repository,
):
    chapter = repository.get_chapter(
        "chapter-1",
    )

    assert chapter.identifier == "chapter-1"


def test_repository_resolves_sloka_by_canonical_id(
    repository,
):
    sloka = repository.get_sloka(
        "sloka-2",
    )

    assert sloka.identifier == "sloka-2"


def test_repository_resolves_word_by_canonical_id(
    repository,
):
    word = repository.get_word(
        "word-3",
    )

    assert word.identifier == "word-3"


# =============================================================
# Repository → ReaderPosition
# =============================================================


def test_repository_resolves_chapter_position(
    repository,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    result = repository.resolve_position(
        position,
    )

    assert result.identifier == "chapter-1"


def test_repository_resolves_sloka_position(
    repository,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    result = repository.resolve_position(
        position,
    )

    assert result.identifier == "sloka-1"


def test_repository_resolves_word_position(
    repository,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    result = repository.resolve_position(
        position,
    )

    assert result.identifier == "word-1"


# =============================================================
# Navigator → Repository
# =============================================================


def test_navigator_moves_to_next_chapter(
    navigator,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    result = navigator.next_chapter(
        position,
    )

    assert result is not None
    assert result.identifier == "chapter-2"


def test_navigator_moves_to_previous_chapter(
    navigator,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    result = navigator.previous_chapter(
        position,
    )

    assert result is not None
    assert result.identifier == "chapter-1"


def test_navigator_moves_to_next_sloka(
    navigator,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    result = navigator.next_sloka(
        position,
    )

    assert result is not None
    assert result.identifier == "sloka-2"


def test_navigator_moves_to_previous_sloka(
    navigator,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-2",
    )

    result = navigator.previous_sloka(
        position,
    )

    assert result is not None
    assert result.identifier == "sloka-1"


def test_navigator_moves_to_next_word(
    navigator,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    result = navigator.next_word(
        position,
    )

    assert result is not None
    assert result.identifier == "word-2"


def test_navigator_moves_to_previous_word(
    navigator,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )

    result = navigator.previous_word(
        position,
    )

    assert result is not None
    assert result.identifier == "word-1"


# =============================================================
# ReaderEngine → Repository
# =============================================================


def test_engine_resolves_chapter_through_repository(
    engine,
):
    result = engine.chapter(
        "chapter-1",
    )

    assert result.identifier == "chapter-1"


def test_engine_resolves_sloka_through_repository(
    engine,
):
    result = engine.sloka(
        "sloka-2",
    )

    assert result.identifier == "sloka-2"


def test_engine_resolves_word_through_repository(
    engine,
):
    result = engine.word(
        "word-4",
    )

    assert result.identifier == "word-4"


# =============================================================
# ReaderEngine → Navigator
# =============================================================


def test_engine_moves_to_next_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    result = engine.move_next(
        position,
    )

    assert result is not None
    assert result.identifier == "chapter-2"


def test_engine_moves_to_previous_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    result = engine.move_previous(
        position,
    )

    assert result is not None
    assert result.identifier == "chapter-1"


def test_engine_moves_to_next_sloka(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    result = engine.move_next(
        position,
    )

    assert result is not None
    assert result.identifier == "sloka-2"


def test_engine_moves_to_next_word(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    result = engine.move_next(
        position,
    )

    assert result is not None
    assert result.identifier == "word-2"


# =============================================================
# Boundary Behaviour
# =============================================================


def test_engine_returns_none_after_last_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )

    result = engine.move_next(
        position,
    )

    assert result is None


def test_engine_returns_none_before_first_chapter(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
    )

    result = engine.move_previous(
        position,
    )

    assert result is None


def test_engine_returns_none_after_last_word(
    engine,
):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
        sloka_id="sloka-3",
        word_id="word-6",
    )

    result = engine.move_next(
        position,
    )

    assert result is None


# =============================================================
# Corpus → Reader → Navigation Consistency
# =============================================================


def test_reader_preserves_corpus_hierarchy_order(
    engine,
):
    chapters = engine.document().chapters

    assert [
        chapter.identifier
        for chapter in chapters
    ] == [
        "chapter-1",
        "chapter-2",
    ]


def test_reader_preserves_sloka_order(
    engine,
):
    slokas = engine.chapter(
        "chapter-1",
    ).slokas

    assert [
        sloka.identifier
        for sloka in slokas
    ] == [
        "sloka-1",
        "sloka-2",
    ]


def test_reader_preserves_word_order(
    engine,
):
    words = engine.sloka(
        "sloka-1",
    ).words

    assert [
        word.identifier
        for word in words
    ] == [
        "word-1",
        "word-2",
    ]

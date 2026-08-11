from __future__ import annotations

"""
SanskritAI
==========

DefaultReaderRepository Navigation Tests

Verifies that the concrete Reader repository correctly exposes
canonical next/previous navigation over the Reader projection.
"""

import pytest

from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata

from SanskritAI.domain.reader.default_reader_repository import (
    DefaultReaderRepository,
)


def _build_corpus():
    """
    Build a minimal corpus containing three chapters and
    three ślokas per chapter.

    Detailed paragraph/line/token construction is intentionally
    omitted here because these tests focus on chapter/śloka
    repository navigation.
    """

    corpus = Corpus(
        id="purana-1",
        metadata=CorpusMetadata(),
    )

    document = Document(
        identifier="document-1",
        metadata=DocumentMetadata(),
    )

    for chapter_number in range(1, 4):

        section = Section(
            identifier=f"chapter-{chapter_number}",
            metadata=SectionMetadata(),
        )

        for sloka_number in range(1, 4):

            verse = Verse(
                identifier=(
                    f"chapter-{chapter_number}"
                    f"-sloka-{sloka_number}"
                ),
                metadata=VerseMetadata(),
            )

            section.add_verse(
                verse
            )

        document.add_section(
            section
        )

    corpus.add_document(
        document
    )

    return corpus


@pytest.fixture
def repository():
    return DefaultReaderRepository(
        corpus=_build_corpus()
    )


# =============================================================
# Chapter Navigation
# =============================================================


def test_next_chapter(repository):
    result = repository.next_chapter(
        "chapter-1"
    )

    assert result is not None
    assert result.identifier == "chapter-2"


def test_previous_chapter(repository):
    result = repository.previous_chapter(
        "chapter-2"
    )

    assert result is not None
    assert result.identifier == "chapter-1"


def test_first_chapter_has_no_previous(repository):
    assert (
        repository.previous_chapter(
            "chapter-1"
        )
        is None
    )


def test_last_chapter_has_no_next(repository):
    assert (
        repository.next_chapter(
            "chapter-3"
        )
        is None
    )


# =============================================================
# Śloka Navigation
# =============================================================


def test_next_sloka(repository):
    result = repository.next_sloka(
        "chapter-1-sloka-1"
    )

    assert result is not None
    assert (
        result.identifier
        == "chapter-1-sloka-2"
    )


def test_previous_sloka(repository):
    result = repository.previous_sloka(
        "chapter-1-sloka-2"
    )

    assert result is not None
    assert (
        result.identifier
        == "chapter-1-sloka-1"
    )


def test_first_sloka_has_no_previous(repository):
    assert (
        repository.previous_sloka(
            "chapter-1-sloka-1"
        )
        is None
    )


def test_last_sloka_has_no_next(repository):
    assert (
        repository.next_sloka(
            "chapter-3-sloka-3"
        )
        is None
    )


# =============================================================
# Invalid IDs
# =============================================================


def test_unknown_chapter_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.next_chapter(
            "chapter-does-not-exist"
        )


def test_unknown_sloka_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.next_sloka(
            "sloka-does-not-exist"
        )

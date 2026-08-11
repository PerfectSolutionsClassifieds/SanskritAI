from __future__ import annotations

"""
SanskritAI
==========

ReaderEngine Tests

Tests the ReaderEngine as a thin façade over:

    ReaderRepository
    ReaderNavigator

These tests intentionally verify delegation rather than Corpus
implementation details.

Version
-------
v1.0.0
"""

from unittest.mock import Mock

import pytest

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


# =============================================================
# Fixtures
# =============================================================


@pytest.fixture
def repository():
    """
    Mock ReaderRepository.
    """

    return Mock()


@pytest.fixture
def navigator():
    """
    Mock ReaderNavigator.
    """

    return Mock()


@pytest.fixture
def engine(
    repository,
    navigator,
):
    """
    ReaderEngine with mocked collaborators.
    """

    return ReaderEngine(
        repository=repository,
        navigator=navigator,
    )


@pytest.fixture
def chapter_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )


@pytest.fixture
def sloka_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )


@pytest.fixture
def word_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )


# =============================================================
# Document Delegation
# =============================================================


def test_document_delegates_to_repository(
    engine,
    repository,
):
    expected = object()

    repository.get_document.return_value = expected

    result = engine.document(
        "document-1",
    )

    assert result is expected

    repository.get_document.assert_called_once_with(
        "document-1",
    )


def test_document_without_id_delegates_to_repository(
    engine,
    repository,
):
    expected = object()

    repository.get_document.return_value = expected

    result = engine.document()

    assert result is expected

    repository.get_document.assert_called_once_with(
        None,
    )


# =============================================================
# Chapter Delegation
# =============================================================


def test_chapter_delegates_to_repository(
    engine,
    repository,
):
    expected = object()

    repository.get_chapter.return_value = expected

    result = engine.chapter(
        "chapter-1",
    )

    assert result is expected

    repository.get_chapter.assert_called_once_with(
        "chapter-1",
    )


# =============================================================
# Śloka Delegation
# =============================================================


def test_sloka_delegates_to_repository(
    engine,
    repository,
):
    expected = object()

    repository.get_sloka.return_value = expected

    result = engine.sloka(
        "sloka-1",
    )

    assert result is expected

    repository.get_sloka.assert_called_once_with(
        "sloka-1",
    )


# =============================================================
# Word Delegation
# =============================================================


def test_word_delegates_to_repository(
    engine,
    repository,
):
    expected = object()

    repository.get_word.return_value = expected

    result = engine.word(
        "word-1",
    )

    assert result is expected

    repository.get_word.assert_called_once_with(
        "word-1",
    )


# =============================================================
# Chapter Navigation
# =============================================================


def test_next_chapter_delegates_to_navigator(
    engine,
    navigator,
    chapter_position,
):
    expected = object()

    navigator.next_chapter.return_value = expected

    result = engine.next_chapter(
        chapter_position,
    )

    assert result is expected

    navigator.next_chapter.assert_called_once_with(
        chapter_position,
    )


def test_previous_chapter_delegates_to_navigator(
    engine,
    navigator,
    chapter_position,
):
    expected = object()

    navigator.previous_chapter.return_value = expected

    result = engine.previous_chapter(
        chapter_position,
    )

    assert result is expected

    navigator.previous_chapter.assert_called_once_with(
        chapter_position,
    )


# =============================================================
# Śloka Navigation
# =============================================================


def test_next_sloka_delegates_to_navigator(
    engine,
    navigator,
    sloka_position,
):
    expected = object()

    navigator.next_sloka.return_value = expected

    result = engine.next_sloka(
        sloka_position,
    )

    assert result is expected

    navigator.next_sloka.assert_called_once_with(
        sloka_position,
    )


def test_previous_sloka_delegates_to_navigator(
    engine,
    navigator,
    sloka_position,
):
    expected = object()

    navigator.previous_sloka.return_value = expected

    result = engine.previous_sloka(
        sloka_position,
    )

    assert result is expected

    navigator.previous_sloka.assert_called_once_with(
        sloka_position,
    )


# =============================================================
# Word Navigation
# =============================================================


def test_next_word_delegates_to_navigator(
    engine,
    navigator,
    word_position,
):
    expected = object()

    navigator.next_word.return_value = expected

    result = engine.next_word(
        word_position,
    )

    assert result is expected

    navigator.next_word.assert_called_once_with(
        word_position,
    )


def test_previous_word_delegates_to_navigator(
    engine,
    navigator,
    word_position,
):
    expected = object()

    navigator.previous_word.return_value = expected

    result = engine.previous_word(
        word_position,
    )

    assert result is expected

    navigator.previous_word.assert_called_once_with(
        word_position,
    )


# =============================================================
# Position Resolution
# =============================================================


def test_resolve_delegates_to_repository_position_resolver(
    engine,
    repository,
    word_position,
):
    expected = object()

    repository.resolve_position.return_value = expected

    result = engine.resolve(
        word_position,
    )

    assert result is expected

    repository.resolve_position.assert_called_once_with(
        word_position,
    )


# =============================================================
# Generic Forward Navigation
# =============================================================


def test_move_next_uses_word_navigation_for_word_position(
    engine,
    navigator,
    word_position,
):
    expected = object()

    navigator.next_word.return_value = expected

    result = engine.move_next(
        word_position,
    )

    assert result is expected

    navigator.next_word.assert_called_once_with(
        word_position,
    )

    navigator.next_sloka.assert_not_called()
    navigator.next_chapter.assert_not_called()


def test_move_next_uses_sloka_navigation_for_sloka_position(
    engine,
    navigator,
    sloka_position,
):
    expected = object()

    navigator.next_sloka.return_value = expected

    result = engine.move_next(
        sloka_position,
    )

    assert result is expected

    navigator.next_sloka.assert_called_once_with(
        sloka_position,
    )

    navigator.next_word.assert_not_called()
    navigator.next_chapter.assert_not_called()


def test_move_next_uses_chapter_navigation_for_chapter_position(
    engine,
    navigator,
    chapter_position,
):
    expected = object()

    navigator.next_chapter.return_value = expected

    result = engine.move_next(
        chapter_position,
    )

    assert result is expected

    navigator.next_chapter.assert_called_once_with(
        chapter_position,
    )

    navigator.next_word.assert_not_called()
    navigator.next_sloka.assert_not_called()


# =============================================================
# Generic Backward Navigation
# =============================================================


def test_move_previous_uses_word_navigation_for_word_position(
    engine,
    navigator,
    word_position,
):
    expected = object()

    navigator.previous_word.return_value = expected

    result = engine.move_previous(
        word_position,
    )

    assert result is expected

    navigator.previous_word.assert_called_once_with(
        word_position,
    )

    navigator.previous_sloka.assert_not_called()
    navigator.previous_chapter.assert_not_called()


def test_move_previous_uses_sloka_navigation_for_sloka_position(
    engine,
    navigator,
    sloka_position,
):
    expected = object()

    navigator.previous_sloka.return_value = expected

    result = engine.move_previous(
        sloka_position,
    )

    assert result is expected

    navigator.previous_sloka.assert_called_once_with(
        sloka_position,
    )

    navigator.previous_word.assert_not_called()
    navigator.previous_chapter.assert_not_called()


def test_move_previous_uses_chapter_navigation_for_chapter_position(
    engine,
    navigator,
    chapter_position,
):
    expected = object()

    navigator.previous_chapter.return_value = expected

    result = engine.move_previous(
        chapter_position,
    )

    assert result is expected

    navigator.previous_chapter.assert_called_once_with(
        chapter_position,
    )

    navigator.previous_word.assert_not_called()
    navigator.previous_sloka.assert_not_called()


# =============================================================
# Navigation Boundary
# =============================================================


def test_move_next_returns_none_at_boundary(
    engine,
    navigator,
    chapter_position,
):
    navigator.next_chapter.return_value = None

    result = engine.move_next(
        chapter_position,
    )

    assert result is None

    navigator.next_chapter.assert_called_once_with(
        chapter_position,
    )


def test_move_previous_returns_none_at_boundary(
    engine,
    navigator,
    chapter_position,
):
    navigator.previous_chapter.return_value = None

    result = engine.move_previous(
        chapter_position,
    )

    assert result is None

    navigator.previous_chapter.assert_called_once_with(
        chapter_position,
    )

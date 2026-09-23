from __future__ import annotations

"""
SanskritAI
==========

ReaderNavigator Tests

Verifies canonical-ID navigation and ReaderPositionFactory
integration.

The tests intentionally use a repository stub so that the
Navigator is tested independently from Corpus construction.
"""

from dataclasses import dataclass

from SanskritAI.domain.reader.reader_navigator import (
    ReaderNavigator,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_position_factory import (
    ReaderPositionFactory,
)


# =============================================================
# Test Objects
# =============================================================


@dataclass(frozen=True)
class FakeView:
    identifier: str
    position: ReaderPosition


class FakeRepository:
    """
    Minimal ReaderRepository-compatible test double.
    """

    def __init__(self):
        self.calls = []

        self.chapters = {
            "chapter-1": FakeView(
                "chapter-1",
                ReaderPositionFactory.chapter(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                ),
            ),
            "chapter-2": FakeView(
                "chapter-2",
                ReaderPositionFactory.chapter(
                    purana_id="purana-1",
                    chapter_id="chapter-2",
                ),
            ),
            "chapter-3": FakeView(
                "chapter-3",
                ReaderPositionFactory.chapter(
                    purana_id="purana-1",
                    chapter_id="chapter-3",
                ),
            ),
        }

        self.slokas = {
            "sloka-1": FakeView(
                "sloka-1",
                ReaderPositionFactory.sloka(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                ),
            ),
            "sloka-2": FakeView(
                "sloka-2",
                ReaderPositionFactory.sloka(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-2",
                ),
            ),
            "sloka-3": FakeView(
                "sloka-3",
                ReaderPositionFactory.sloka(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-3",
                ),
            ),
        }

        self.words = {
            "word-1": FakeView(
                "word-1",
                ReaderPositionFactory.word(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                    word_id="word-1",
                ),
            ),
            "word-2": FakeView(
                "word-2",
                ReaderPositionFactory.word(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                    word_id="word-2",
                ),
            ),
            "word-3": FakeView(
                "word-3",
                ReaderPositionFactory.word(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                    word_id="word-3",
                ),
            ),
        }

    # ---------------------------------------------------------
    # Chapter
    # ---------------------------------------------------------

    def next_chapter(self, chapter_id):
        self.calls.append(
            ("next_chapter", chapter_id)
        )

        order = [
            "chapter-1",
            "chapter-2",
            "chapter-3",
        ]

        try:
            index = order.index(str(chapter_id))
        except ValueError:
            raise KeyError(chapter_id)

        if index + 1 >= len(order):
            return None

        return self.chapters[
            order[index + 1]
        ]

    def previous_chapter(self, chapter_id):
        self.calls.append(
            ("previous_chapter", chapter_id)
        )

        order = [
            "chapter-1",
            "chapter-2",
            "chapter-3",
        ]

        try:
            index = order.index(str(chapter_id))
        except ValueError:
            raise KeyError(chapter_id)

        if index == 0:
            return None

        return self.chapters[
            order[index - 1]
        ]

    # ---------------------------------------------------------
    # Śloka
    # ---------------------------------------------------------

    def next_sloka(self, sloka_id):
        self.calls.append(
            ("next_sloka", sloka_id)
        )

        order = [
            "sloka-1",
            "sloka-2",
            "sloka-3",
        ]

        index = order.index(
            str(sloka_id)
        )

        if index + 1 >= len(order):
            return None

        return self.slokas[
            order[index + 1]
        ]

    def previous_sloka(self, sloka_id):
        self.calls.append(
            ("previous_sloka", sloka_id)
        )

        order = [
            "sloka-1",
            "sloka-2",
            "sloka-3",
        ]

        index = order.index(
            str(sloka_id)
        )

        if index == 0:
            return None

        return self.slokas[
            order[index - 1]
        ]

    # ---------------------------------------------------------
    # Word
    # ---------------------------------------------------------

    def next_word(self, word_id):
        self.calls.append(
            ("next_word", word_id)
        )

        order = [
            "word-1",
            "word-2",
            "word-3",
        ]

        index = order.index(
            str(word_id)
        )

        if index + 1 >= len(order):
            return None

        return self.words[
            order[index + 1]
        ]

    def previous_word(self, word_id):
        self.calls.append(
            ("previous_word", word_id)
        )

        order = [
            "word-1",
            "word-2",
            "word-3",
        ]

        index = order.index(
            str(word_id)
        )

        if index == 0:
            return None

        return self.words[
            order[index - 1]
        ]


# =============================================================
# Fixtures
# =============================================================


def make_navigator():
    repository = FakeRepository()

    navigator = ReaderNavigator(
        repository=repository,
        position_factory=ReaderPositionFactory(),
    )

    return navigator, repository


# =============================================================
# Chapter Tests
# =============================================================


def test_next_chapter_uses_canonical_id():
    navigator, repository = make_navigator()

    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    result = navigator.next_chapter(
        current
    )

    assert result is not None
    assert result.chapter_id == "chapter-2"
    assert result.purana_id == "purana-1"

    assert repository.calls[-1] == (
        "next_chapter",
        "chapter-1",
    )


def test_previous_chapter_uses_canonical_id():
    navigator, repository = make_navigator()

    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )

    result = navigator.previous_chapter(
        current
    )

    assert result is not None
    assert result.chapter_id == "chapter-1"
    assert result.purana_id == "purana-1"

    assert repository.calls[-1] == (
        "previous_chapter",
        "chapter-2",
    )


def test_first_chapter_has_no_previous():
    navigator, _ = make_navigator()

    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert (
        navigator.previous_chapter(current)
        is None
    )


def test_last_chapter_has_no_next():
    navigator, _ = make_navigator()

    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-3",
    )

    assert (
        navigator.next_chapter(current)
        is None
    )


# =============================================================
# Śloka Tests
# =============================================================


def test_next_sloka_constructs_factory_position():
    navigator, repository = make_navigator()

    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    result = navigator.next_sloka(
        current
    )

    assert result is not None
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-2"

    assert repository.calls[-1] == (
        "next_sloka",
        "sloka-1",
    )


def test_previous_sloka_constructs_factory_position():
    navigator, repository = make_navigator()

    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-2",
    )

    result = navigator.previous_sloka(
        current
    )

    assert result is not None
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"

    assert repository.calls[-1] == (
        "previous_sloka",
        "sloka-2",
    )


def test_last_sloka_has_no_next():
    navigator, _ = make_navigator()

    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-3",
    )

    assert (
        navigator.next_sloka(current)
        is None
    )


# =============================================================
# Word Tests
# =============================================================


def test_next_word_preserves_structural_context():
    navigator, repository = make_navigator()

    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    result = navigator.next_word(
        current
    )

    assert result is not None

    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert result.word_id == "word-2"

    assert repository.calls[-1] == (
        "next_word",
        "word-1",
    )


def test_previous_word_preserves_structural_context():
    navigator, repository = make_navigator()

    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )

    result = navigator.previous_word(
        current
    )

    assert result is not None

    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert result.word_id == "word-1"

    assert repository.calls[-1] == (
        "previous_word",
        "word-2",
    )


def test_first_word_has_no_previous():
    navigator, _ = make_navigator()

    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert (
        navigator.previous_word(current)
        is None
    )


def test_last_word_has_no_next():
    navigator, _ = make_navigator()

    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-3",
    )

    assert (
        navigator.next_word(current)
        is None
    )


# =============================================================
# Immutability / No-Index Contract
# =============================================================


def test_navigation_returns_new_immutable_position():
    navigator, _ = make_navigator()

    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    result = navigator.next_chapter(
        current
    )

    assert result is not current

    # ReaderPosition should be immutable.
    try:
        result.chapter_id = "chapter-x"
    except Exception:
        pass
    else:
        raise AssertionError(
            "ReaderPosition must be immutable."
        )


def test_navigator_does_not_require_indices():
    """
    The Reader navigation contract is identifier-based.

    This test intentionally constructs a position without any
    chapter/sloka/word index attributes.
    """

    navigator, _ = make_navigator()

    position = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    assert not hasattr(
        position,
        "chapter_index",
    )

    assert not hasattr(
        position,
        "sloka_index",
    )

    assert not hasattr(
        position,
        "word_index",
    )

    result = navigator.next_sloka(
        position
    )

    assert result.sloka_id == "sloka-2"

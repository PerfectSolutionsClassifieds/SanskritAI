
from __future__ import annotations

"""
SanskritAI
==========

ReaderSession ↔ ReaderSessionHistory Integration Tests

Controlled integration boundary:

    ReaderEngine
        │
        ├── next / previous
        │
        ▼
    ReaderSession
        │
        └── ReaderSessionHistory
              ├── back
              └── forward

The current ReaderSession is a mutable session façade.

Therefore these tests intentionally use:

    ReaderSession(
        engine=engine,
        history=history,
    )

and:

    session.set_position(...)

They do NOT use the obsolete class-style:

    ReaderSession.open(...)

or:

    session.open(...)

Version
-------
v1.0.0
"""

import pytest

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
# Fixtures
# =============================================================


@pytest.fixture
def history() -> ReaderSessionHistory:
    """
    Provide a fresh session-history object for every test.
    """

    return ReaderSessionHistory()


@pytest.fixture
def session(
    engine,
    history,
) -> ReaderSession:
    """
    Construct the current mutable ReaderSession implementation.
    """

    return ReaderSession(
        engine=engine,
        history=history,
    )


# =============================================================
# Helpers
# =============================================================


def chapter_position(
    chapter_id: str,
) -> ReaderPosition:
    return ReaderPosition(
        purana_id="corpus-1",
        chapter_id=chapter_id,
    )


def sloka_position(
    sloka_id: str,
) -> ReaderPosition:
    return ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id=sloka_id,
    )


def word_position(
    word_id: str,
) -> ReaderPosition:
    return ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id=word_id,
    )


# =============================================================
# Initial Session State
# =============================================================


def test_session_starts_without_position(
    session,
):
    assert session.current_position is None
    assert session.has_position is False
    assert session.history_count == 0
    assert session.can_go_back is False
    assert session.can_go_forward is False


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
# Position Management
# =============================================================


def test_set_position_establishes_initial_position(
    session,
):
    position = chapter_position(
        "chapter-1",
    )

    result = session.set_position(
        position,
    )

    assert result == position
    assert session.current_position == position
    assert session.has_position is True


def test_set_position_records_initial_position_in_history(
    session,
):
    position = chapter_position(
        "chapter-1",
    )

    session.set_position(
        position,
    )

    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False


def test_set_position_creates_new_history_root(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()

    assert session.current_position == chapter_2
    assert session.history_count == 2

    session.set_position(
        chapter_1,
    )

    assert session.current_position == chapter_1
    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False


# =============================================================
# ReaderEngine Structural Navigation
# =============================================================


def test_session_next_delegates_to_reader_engine(
    session,
):
    initial = chapter_position(
        "chapter-1",
    )

    expected = chapter_position(
        "chapter-2",
    )

    session.set_position(
        initial,
    )

    result = session.next()

    assert result == expected
    assert session.current_position == expected


def test_session_next_records_result_in_history(
    session,
):
    initial = chapter_position(
        "chapter-1",
    )

    expected = chapter_position(
        "chapter-2",
    )

    session.set_position(
        initial,
    )

    session.next()

    assert session.history_count == 2
    assert session.can_go_back is True
    assert session.can_go_forward is False

    back_result = session.back()

    assert back_result == initial
    assert session.current_position == initial


def test_session_previous_delegates_to_reader_engine(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_2,
    )

    result = session.previous()

    assert result == chapter_1
    assert session.current_position == chapter_1


def test_session_previous_records_result_in_history(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_2,
    )

    session.previous()

    assert session.current_position == chapter_1
    assert session.history_count == 2


def test_session_next_returns_none_at_engine_boundary(
    session,
):
    last_chapter = chapter_position(
        "chapter-2",
    )

    session.set_position(
        last_chapter,
    )

    result = session.next()

    assert result is None
    assert session.current_position == last_chapter
    assert session.history_count == 1


def test_session_previous_returns_none_at_engine_boundary(
    session,
):
    first_chapter = chapter_position(
        "chapter-1",
    )

    session.set_position(
        first_chapter,
    )

    result = session.previous()

    assert result is None
    assert session.current_position == first_chapter
    assert session.history_count == 1


# =============================================================
# History Navigation
# =============================================================


def test_session_back_uses_history(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()

    assert session.current_position == chapter_2

    result = session.back()

    assert result == chapter_1
    assert session.current_position == chapter_1


def test_session_forward_uses_history(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()
    session.back()

    assert session.current_position == chapter_1
    assert session.can_go_forward is True

    result = session.forward()

    assert result == chapter_2
    assert session.current_position == chapter_2


def test_session_back_returns_none_at_history_root(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    session.set_position(
        chapter_1,
    )

    result = session.back()

    assert result is None
    assert session.current_position == chapter_1


def test_session_forward_returns_none_without_forward_history(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    session.set_position(
        chapter_1,
    )

    result = session.forward()

    assert result is None
    assert session.current_position == chapter_1


def test_session_history_round_trip(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()

    assert session.current_position == chapter_2

    assert session.back() == chapter_1
    assert session.current_position == chapter_1

    assert session.forward() == chapter_2
    assert session.current_position == chapter_2


# =============================================================
# Forward-history Truncation
# =============================================================


def test_new_position_clears_forward_history(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()

    assert session.current_position == chapter_2

    session.back()

    assert session.current_position == chapter_1
    assert session.can_go_forward is True

    chapter_2_again = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_2_again,
    )

    assert session.current_position == chapter_2_again
    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False


# =============================================================
# Śloka-level Navigation
# =============================================================


def test_session_history_tracks_sloka_navigation(
    session,
):
    sloka_1 = sloka_position(
        "sloka-1",
    )

    sloka_2 = sloka_position(
        "sloka-2",
    )

    session.set_position(
        sloka_1,
    )

    result = session.next()

    assert result == sloka_2
    assert session.current_position == sloka_2
    assert session.history_count == 2

    assert session.back() == sloka_1
    assert session.current_position == sloka_1

    assert session.forward() == sloka_2
    assert session.current_position == sloka_2


# =============================================================
# Word-level Navigation
# =============================================================


def test_session_history_tracks_word_navigation(
    session,
):
    word_1 = word_position(
        "word-1",
    )

    word_2 = word_position(
        "word-2",
    )

    session.set_position(
        word_1,
    )

    result = session.next()

    assert result == word_2
    assert session.current_position == word_2
    assert session.history_count == 2

    assert session.back() == word_1
    assert session.current_position == word_1

    assert session.forward() == word_2
    assert session.current_position == word_2


# =============================================================
# History Control
# =============================================================


def test_session_can_clear_history(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()

    assert session.history_count == 2

    session.clear_history()

    assert session.history_count == 0
    assert session.can_go_back is False
    assert session.can_go_forward is False

    # Clearing history must not erase the session's
    # current structural position.
    assert session.current_position == chapter_2


# =============================================================
# Separation of Responsibilities
# =============================================================


def test_history_back_and_engine_navigation_remain_distinct(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    # Establish session root.
    session.set_position(
        chapter_1,
    )

    # Structural navigation uses ReaderEngine.
    engine_result = session.next()

    assert engine_result == chapter_2
    assert session.current_position == chapter_2

    # History navigation returns to the previous
    # browsing position without structural navigation.
    history_result = session.back()

    assert history_result == chapter_1
    assert session.current_position == chapter_1

    # Structural navigation can again move forward.
    engine_result = session.next()

    assert engine_result == chapter_2
    assert session.current_position == chapter_2


def test_history_state_reflects_current_session_position(
    session,
):
    chapter_1 = chapter_position(
        "chapter-1",
    )

    chapter_2 = chapter_position(
        "chapter-2",
    )

    session.set_position(
        chapter_1,
    )

    session.next()

    assert session.current_position == chapter_2
    assert session.can_go_back is True
    assert session.can_go_forward is False

    session.back()

    assert session.current_position == chapter_1
    assert session.can_go_back is False
    assert session.can_go_forward is True

    session.forward()

    assert session.current_position == chapter_2
    assert session.can_go_back is True
    assert session.can_go_forward is False

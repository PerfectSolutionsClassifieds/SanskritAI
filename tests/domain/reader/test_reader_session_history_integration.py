
from unittest.mock import Mock

import pytest

from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session import ReaderSession
from SanskritAI.domain.reader.reader_session_history import (
    ReaderSessionHistory,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def engine():
    """
    Mock ReaderEngine used by ReaderSession for structural
    navigation.
    """
    return Mock(spec=ReaderEngine)


@pytest.fixture
def history():
    """
    Real ReaderSessionHistory.

    This is intentionally NOT mocked because this file verifies
    integration between ReaderSession and ReaderSessionHistory.
    """
    return ReaderSessionHistory()


@pytest.fixture
def position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )


@pytest.fixture
def next_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )


@pytest.fixture
def previous_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-0",
    )


@pytest.fixture
def session(
    engine,
    history,
):
    """
    Create an empty ReaderSession with injected dependencies.
    """
    return ReaderSession(
        engine=engine,
        history=history,
    )


# ============================================================
# Initial Session State
# ============================================================

def test_session_starts_without_position(
    session,
):
    assert session.current_position is None
    assert session.has_position is False
    assert session.history_count == 0
    assert session.can_go_back is False
    assert session.can_go_forward is False


def test_session_uses_injected_history_instance(
    session,
    history,
):
    assert session.history is history


# ============================================================
# set_position()
# ============================================================

def test_set_position_establishes_initial_position(
    session,
    position,
):
    result = session.set_position(
        position,
    )

    assert result == position
    assert session.current_position == position
    assert session.has_position is True


def test_set_position_records_initial_position_in_history(
    session,
    position,
):
    session.set_position(
        position,
    )

    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False


def test_set_position_creates_new_history_root(
    session,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    session.history.push(
        next_position,
    )

    assert session.history_count == 2

    session.set_position(
        next_position,
    )

    assert session.current_position == next_position
    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False


# ============================================================
# next()
# ============================================================

def test_session_next_delegates_to_reader_engine(
    session,
    engine,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    engine.move_next.return_value = (
        next_position
    )

    result = session.next()

    engine.move_next.assert_called_once_with(
        position,
    )

    assert result == next_position
    assert session.current_position == next_position


def test_session_next_records_result_in_history(
    session,
    engine,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    engine.move_next.return_value = (
        next_position
    )

    session.next()

    assert session.history_count == 2

    assert session.history.can_go_back is True


def test_session_next_returns_none_at_engine_boundary(
    session,
    engine,
    position,
):
    session.set_position(
        position,
    )

    engine.move_next.return_value = None

    result = session.next()

    assert result is None
    assert session.current_position == position
    assert session.history_count == 1


# ============================================================
# previous()
# ============================================================

def test_session_previous_delegates_to_reader_engine(
    session,
    engine,
    position,
    previous_position,
):
    session.set_position(
        position,
    )

    engine.move_previous.return_value = (
        previous_position
    )

    result = session.previous()

    engine.move_previous.assert_called_once_with(
        position,
    )

    assert result == previous_position
    assert session.current_position == previous_position


def test_session_previous_records_result_in_history(
    session,
    engine,
    position,
    previous_position,
):
    session.set_position(
        position,
    )

    engine.move_previous.return_value = (
        previous_position
    )

    session.previous()

    assert session.history_count == 2
    assert session.current_position == previous_position


def test_session_previous_returns_none_at_engine_boundary(
    session,
    engine,
    position,
):
    session.set_position(
        position,
    )

    engine.move_previous.return_value = None

    result = session.previous()

    assert result is None
    assert session.current_position == position
    assert session.history_count == 1


# ============================================================
# back()
# ============================================================

def test_session_back_uses_history(
    session,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    session.history.push(
        next_position,
    )

    session.position = next_position

    result = session.back()

    assert result == position
    assert session.current_position == position


def test_session_back_returns_none_at_history_root(
    session,
    position,
):
    session.set_position(
        position,
    )

    result = session.back()

    assert result is None
    assert session.current_position == position


# ============================================================
# forward()
# ============================================================

def test_session_forward_uses_history(
    session,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    session.history.push(
        next_position,
    )

    session.position = next_position

    result = session.back()

    assert result == position
    assert session.current_position == position

    result = session.forward()

    assert result == next_position
    assert session.current_position == next_position


def test_session_forward_returns_none_without_forward_history(
    session,
    position,
):
    session.set_position(
        position,
    )

    result = session.forward()

    assert result is None
    assert session.current_position == position


# ============================================================
# History Round Trip
# ============================================================

def test_session_history_round_trip(
    session,
    position,
    next_position,
    previous_position,
):
    session.set_position(
        position,
    )

    session.history.push(
        next_position,
    )

    session.history.push(
        previous_position,
    )

    session.position = previous_position

    assert session.current_position == previous_position

    assert session.back() == next_position
    assert session.current_position == next_position

    assert session.back() == position
    assert session.current_position == position

    assert session.forward() == next_position
    assert session.current_position == next_position

    assert session.forward() == previous_position
    assert session.current_position == previous_position


# ============================================================
# New Position / Forward History
# ============================================================

def test_new_position_clears_forward_history(
    session,
    position,
    next_position,
    previous_position,
):
    session.set_position(
        position,
    )

    session.history.push(
        next_position,
    )

    session.position = next_position

    assert session.back() == position
    assert session.current_position == position
    assert session.can_go_forward is True

    session.set_position(
        previous_position,
    )

    assert session.current_position == previous_position
    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False


# ============================================================
# Structural Navigation + History Integration
# ============================================================

def test_session_history_tracks_sloka_navigation(
    session,
    engine,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    engine.move_next.return_value = (
        next_position
    )

    result = session.next()

    assert result == next_position
    assert session.current_position == next_position
    assert session.history_count == 2

    assert session.back() == position
    assert session.current_position == position

    assert session.forward() == next_position
    assert session.current_position == next_position


def test_session_history_tracks_word_navigation(
    session,
    engine,
):
    position_1 = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    position_2 = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )

    position_3 = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-3",
    )

    session.set_position(
        position_1,
    )

    engine.move_next.side_effect = [
        position_2,
        position_3,
    ]

    assert session.next() == position_2
    assert session.next() == position_3

    assert session.history_count == 3

    assert session.back() == position_2
    assert session.back() == position_1

    assert session.forward() == position_2
    assert session.forward() == position_3


# ============================================================
# clear_history()
# ============================================================

def test_session_can_clear_history(
    session,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    session.history.push(
        next_position,
    )

    session.position = next_position

    assert session.history_count == 2

    session.clear_history()

    assert session.history_count == 0
    assert session.can_go_back is False
    assert session.can_go_forward is False

    # Clearing history does not itself erase the current
    # session position.
    assert session.current_position == next_position


# ============================================================
# Distinction Between Engine Navigation and History Navigation
# ============================================================

def test_history_back_and_engine_navigation_remain_distinct(
    session,
    engine,
    position,
    next_position,
    previous_position,
):
    session.set_position(
        position,
    )

    engine.move_next.return_value = (
        next_position
    )

    engine.move_previous.return_value = (
        previous_position
    )

    # Structural navigation asks the ReaderEngine.
    assert session.next() == next_position

    engine.move_next.assert_called_once_with(
        position,
    )

    # History navigation does NOT ask the ReaderEngine.
    engine.reset_mock()

    assert session.back() == position

    engine.move_next.assert_not_called()
    engine.move_previous.assert_not_called()

    # Structural previous navigation again asks the engine.
    assert session.previous() == previous_position

    engine.move_previous.assert_called_once_with(
        position,
    )


def test_history_state_reflects_current_session_position(
    session,
    engine,
    position,
    next_position,
):
    session.set_position(
        position,
    )

    engine.move_next.return_value = (
        next_position
    )

    session.next()

    assert session.current_position == next_position
    assert session.can_go_back is True
    assert session.can_go_forward is False

    session.back()

    assert session.current_position == position
    assert session.can_go_back is False
    assert session.can_go_forward is True

    session.forward()

    assert session.current_position == next_position
    assert session.can_go_back is True
    assert session.can_go_forward is False

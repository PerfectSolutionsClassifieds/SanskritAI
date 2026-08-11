
from __future__ import annotations

"""
SanskritAI
==========

ReaderSessionHistory Unit Tests

Locks down the observable contract of ReaderSessionHistory before
integrating it into ReaderSession.

The tests intentionally avoid inspecting private implementation
details such as:

    _back_stack
    _current
    _forward_stack

The tests verify only externally observable behaviour.

Version
-------
v1.0.0
"""

import pytest

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_session_history import (
    ReaderSessionHistory,
)


# =============================================================
# Fixtures
# =============================================================


@pytest.fixture
def position_a() -> ReaderPosition:
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )


@pytest.fixture
def position_b() -> ReaderPosition:
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )


@pytest.fixture
def position_c() -> ReaderPosition:
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-3",
    )


@pytest.fixture
def position_d() -> ReaderPosition:
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-4",
    )


# =============================================================
# Initial State
# =============================================================


def test_history_starts_empty():
    history = ReaderSessionHistory()

    assert history.current is None
    assert history.position is None

    assert history.has_current is False

    assert history.can_go_back is False
    assert history.can_back is False

    assert history.can_go_forward is False
    assert history.can_forward is False

    assert history.back_count == 0
    assert history.forward_count == 0
    assert history.history_count == 0

    assert history.is_empty is True

    assert history.previous is None
    assert history.next is None


# =============================================================
# First Record
# =============================================================


def test_first_record_becomes_current(
    position_a,
):
    history = ReaderSessionHistory()

    result = history.record(
        position_a,
    )

    assert result is position_a
    assert history.current is position_a
    assert history.position is position_a

    assert history.has_current is True

    assert history.back_count == 0
    assert history.forward_count == 0
    assert history.history_count == 1

    assert history.can_go_back is False
    assert history.can_go_forward is False


# =============================================================
# Sequential Recording
# =============================================================


def test_recording_new_positions_creates_back_history(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    assert history.current is position_c

    assert history.back_count == 2
    assert history.forward_count == 0
    assert history.history_count == 3

    assert history.can_go_back is True
    assert history.can_go_forward is False

    assert history.previous is position_b


# =============================================================
# Duplicate Suppression
# =============================================================


def test_recording_same_position_does_not_create_duplicate(
    position_a,
):
    history = ReaderSessionHistory()

    first = history.record(
        position_a,
    )

    second = history.record(
        position_a,
    )

    assert first is position_a
    assert second is position_a

    assert history.current is position_a

    assert history.back_count == 0
    assert history.forward_count == 0
    assert history.history_count == 1


# =============================================================
# Back Navigation
# =============================================================


def test_back_moves_to_previous_position(
    position_a,
    position_b,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)

    result = history.back()

    assert result is position_a
    assert history.current is position_a

    assert history.back_count == 0
    assert history.forward_count == 1

    assert history.can_go_back is False
    assert history.can_go_forward is True

    assert history.next is position_b


def test_back_moves_through_multiple_positions(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    assert history.back() is position_b
    assert history.back() is position_a

    assert history.current is position_a

    assert history.back_count == 0
    assert history.forward_count == 2

    assert history.can_go_back is False
    assert history.can_go_forward is True


# =============================================================
# Back Boundary
# =============================================================


def test_back_returns_none_at_history_boundary(
    position_a,
):
    history = ReaderSessionHistory()

    history.record(position_a)

    result = history.back()

    assert result is None

    assert history.current is position_a

    assert history.back_count == 0
    assert history.forward_count == 0


def test_back_on_empty_history_returns_none():
    history = ReaderSessionHistory()

    assert history.back() is None

    assert history.current is None
    assert history.is_empty is True


# =============================================================
# Forward Navigation
# =============================================================


def test_forward_restores_previous_position(
    position_a,
    position_b,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)

    assert history.back() is position_a

    result = history.forward()

    assert result is position_b
    assert history.current is position_b

    assert history.back_count == 1
    assert history.forward_count == 0

    assert history.can_go_back is True
    assert history.can_go_forward is False

    assert history.previous is position_a


def test_forward_moves_through_multiple_positions(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    history.back()
    history.back()

    assert history.current is position_a

    assert history.forward() is position_b
    assert history.forward() is position_c

    assert history.current is position_c

    assert history.back_count == 2
    assert history.forward_count == 0


# =============================================================
# Forward Boundary
# =============================================================


def test_forward_returns_none_at_history_boundary(
    position_a,
    position_b,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)

    assert history.forward() is None

    assert history.current is position_b

    assert history.back_count == 1
    assert history.forward_count == 0


def test_forward_on_empty_history_returns_none():
    history = ReaderSessionHistory()

    assert history.forward() is None

    assert history.current is None
    assert history.is_empty is True


# =============================================================
# Back → Forward Round Trip
# =============================================================


def test_back_and_forward_round_trip(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    assert history.back() is position_b
    assert history.back() is position_a

    assert history.forward() is position_b
    assert history.forward() is position_c

    assert history.current is position_c

    assert history.back_count == 2
    assert history.forward_count == 0


# =============================================================
# New Navigation Clears Forward History
# =============================================================


def test_new_record_clears_forward_history(
    position_a,
    position_b,
    position_c,
    position_d,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    # Current:
    #
    # A → B → C

    assert history.back() is position_b

    # Current:
    #
    # A → B ← C
    #
    # C is now forward history.

    assert history.can_go_forward is True
    assert history.next is position_c

    # New branch:
    #
    # A → B → D

    history.record(position_d)

    assert history.current is position_d

    assert history.can_go_forward is False
    assert history.forward_count == 0
    assert history.next is None

    assert history.back() is position_b


# =============================================================
# Peek Properties
# =============================================================


def test_previous_and_next_do_not_modify_history(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    assert history.previous is position_b

    assert history.back_count == 2
    assert history.forward_count == 0

    history.back()

    assert history.previous is position_a
    assert history.next is position_c

    assert history.back_count == 1
    assert history.forward_count == 1

    # Peeking again must not alter state.

    assert history.previous is position_a
    assert history.next is position_c

    assert history.back_count == 1
    assert history.forward_count == 1


# =============================================================
# Clear
# =============================================================


def test_clear_removes_entire_history(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    history.back()

    assert history.history_count == 3

    history.clear()

    assert history.current is None
    assert history.position is None

    assert history.back_count == 0
    assert history.forward_count == 0
    assert history.history_count == 0

    assert history.can_go_back is False
    assert history.can_go_forward is False

    assert history.previous is None
    assert history.next is None

    assert history.is_empty is True


# =============================================================
# Clear Forward
# =============================================================


def test_clear_forward_preserves_current_and_back_history(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    history.back()

    assert history.current is position_b
    assert history.back_count == 1
    assert history.forward_count == 1

    history.clear_forward()

    assert history.current is position_b

    assert history.back_count == 1
    assert history.forward_count == 0

    assert history.can_go_back is True
    assert history.can_go_forward is False

    assert history.previous is position_a
    assert history.next is None


# =============================================================
# Type Safety
# =============================================================


def test_record_rejects_invalid_position():
    history = ReaderSessionHistory()

    with pytest.raises(TypeError):
        history.record(
            "chapter-1",
        )


def test_record_rejects_none():
    history = ReaderSessionHistory()

    with pytest.raises(TypeError):
        history.record(
            None,
        )


# =============================================================
# ReaderPosition Immutability
# =============================================================


def test_history_does_not_mutate_reader_position(
    position_a,
):
    history = ReaderSessionHistory()

    history.record(position_a)

    assert history.current is position_a

    with pytest.raises(
        Exception,
    ):
        position_a.chapter_id = "chapter-x"

    assert history.current.chapter_id == "chapter-1"


# =============================================================
# Display Contract
# =============================================================


def test_display_name():
    history = ReaderSessionHistory()

    assert (
        history.display_name
        == "Reader Session History"
    )


def test_display_text_when_empty():
    history = ReaderSessionHistory()

    assert (
        history.display_text
        == "Reader history is empty"
    )


def test_display_text_when_current_exists(
    position_a,
):
    history = ReaderSessionHistory()

    history.record(position_a)

    assert (
        history.display_text
        == str(position_a)
    )


def test_display_description(
    position_a,
    position_b,
    position_c,
):
    history = ReaderSessionHistory()

    history.record(position_a)
    history.record(position_b)
    history.record(position_c)

    history.back()

    assert (
        history.display_description
        == "1 back, 1 forward"
    )


# =============================================================
# String Representation
# =============================================================


def test_string_representation_when_empty():
    history = ReaderSessionHistory()

    assert str(history) == (
        "Reader history is empty"
    )


def test_string_representation_with_current(
    position_a,
):
    history = ReaderSessionHistory()

    history.record(position_a)

    assert str(history) == str(position_a)

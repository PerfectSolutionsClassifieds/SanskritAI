from __future__ import annotations
"""
SanskritAI
==========
ReaderSession Tests
Locks down the current mutable ReaderSession contract:
• construction and initial state
• current position and history exposure
• open/set_position
• structural next/previous navigation
• session-history back/forward navigation
• navigation boundaries
• history branching
• failed navigation state preservation
• clear_history behaviour
• display contract
• ReaderEngine delegation
Version
-------
v2.0.1
"""
from unittest.mock import Mock
import pytest
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session import ReaderSession

@pytest.fixture
def engine():
    return Mock(spec=ReaderEngine)

@pytest.fixture
def position():
    return ReaderPosition(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-1")

@pytest.fixture
def next_position():
    return ReaderPosition(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-2")

@pytest.fixture
def previous_position():
    return ReaderPosition(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-0")

@pytest.fixture
def another_position():
    return ReaderPosition(purana_id="purana-1",chapter_id="chapter-2")

def make_session(engine,position=None):
    return ReaderSession(engine=engine,position=position)

# =============================================================
# Construction / State
# =============================================================

def test_session_constructs_with_engine(engine):
    session=ReaderSession(engine=engine)
    assert session.engine is engine
    assert session.position is None
    assert session.current_position is None
    assert session.has_position is False
    assert session.history_count == 0

def test_session_accepts_initial_position(engine,position):
    session=ReaderSession(engine=engine,position=position)
    assert session.position is position
    assert session.current_position is position
    assert session.has_position is True
    assert session.history_count == 0

def test_history_defaults_to_new_history_instance(engine):
    a=ReaderSession(engine=engine)
    b=ReaderSession(engine=engine)
    assert a.history is not b.history

def test_can_go_back_initially_false(engine):
    session=ReaderSession(engine=engine)
    assert session.can_go_back is False

def test_can_go_forward_initially_false(engine):
    session=ReaderSession(engine=engine)
    assert session.can_go_forward is False

# =============================================================
# Open / Set Position
# =============================================================

def test_open_establishes_position(engine,position):
    session=ReaderSession(engine=engine)
    result=session.open(position)
    assert result is position
    assert session.position is position
    assert session.current_position is position
    assert session.has_position is True

def test_open_establishes_initial_history_entry(engine,position):
    session=ReaderSession(engine=engine)
    session.open(position)
    assert session.history.current is position
    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False

def test_open_clears_existing_history(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    assert session.history_count == 2
    session.open(position)
    assert session.position is position
    assert session.history.current is position
    assert session.history_count == 1
    assert session.can_go_back is False
    assert session.can_go_forward is False

def test_set_position_establishes_new_root(engine,position,another_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.set_position(another_position)
    assert session.position is another_position
    assert session.history.current is another_position
    assert session.history_count == 1

def test_set_position_none_clears_position_and_history(engine,position):
    session=ReaderSession(engine=engine)
    session.open(position)
    result=session.set_position(None)
    assert result is None
    assert session.position is None
    assert session.current_position is None
    assert session.has_position is False
    assert session.history_count == 0
    assert session.can_go_back is False
    assert session.can_go_forward is False

def test_open_returns_supplied_position(engine,position):
    session=ReaderSession(engine=engine)
    assert session.open(position) is position

# =============================================================
# Next
# =============================================================

def test_next_returns_none_without_position(engine):
    session=ReaderSession(engine=engine)
    assert session.next() is None
    engine.move_next.assert_not_called()

def test_next_delegates_to_engine(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.return_value=next_position
    result=session.next()
    engine.move_next.assert_called_once_with(position)
    assert result is next_position

def test_next_updates_position(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.return_value=next_position
    session.next()
    assert session.position is next_position
    assert session.current_position is next_position

def test_next_records_result_in_history(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.return_value=next_position
    session.next()
    assert session.history.current is next_position
    assert session.history_count == 1

def test_next_returns_none_at_boundary(engine,position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.return_value=None
    result=session.next()
    assert result is None
    assert session.position is position
    assert session.history_count == 0

def test_next_does_not_change_state_when_engine_returns_none(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    session.history.record(next_position)
    before=session.history_count
    engine.move_next.return_value=None
    assert session.next() is None
    assert session.position is position
    assert session.history_count == before

def test_next_can_record_multiple_structural_moves(engine,position,next_position,another_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.side_effect=[next_position,another_position]
    assert session.next() is next_position
    assert session.next() is another_position
    assert session.position is another_position
    assert session.history_count == 2

# =============================================================
# Previous
# =============================================================

def test_previous_returns_none_without_position(engine):
    session=ReaderSession(engine=engine)
    assert session.previous() is None
    engine.move_previous.assert_not_called()

def test_previous_delegates_to_engine(engine,position,previous_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_previous.return_value=previous_position
    result=session.previous()
    engine.move_previous.assert_called_once_with(position)
    assert result is previous_position

def test_previous_updates_position(engine,position,previous_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_previous.return_value=previous_position
    session.previous()
    assert session.position is previous_position

def test_previous_records_result_in_history(engine,position,previous_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_previous.return_value=previous_position
    session.previous()
    assert session.history.current is previous_position
    assert session.history_count == 1

def test_previous_returns_none_at_boundary(engine,position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_previous.return_value=None
    assert session.previous() is None
    assert session.position is position
    assert session.history_count == 0

def test_previous_does_not_change_state_when_engine_returns_none(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    session.history.record(next_position)
    before=session.history_count
    engine.move_previous.return_value=None
    assert session.previous() is None
    assert session.position is position
    assert session.history_count == before

# =============================================================
# Session History Back
# =============================================================

def test_back_delegates_to_history_only(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    result=session.back()
    assert result is position
    assert session.position is position
    engine.move_previous.assert_not_called()
    engine.move_next.assert_not_called()

def test_back_updates_position(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.back()
    assert session.position is position
    assert session.current_position is position

def test_back_returns_none_at_boundary(engine,position):
    session=ReaderSession(engine=engine)
    session.open(position)
    assert session.back() is None
    assert session.position is position

def test_back_preserves_position_at_boundary(engine,position):
    session=ReaderSession(engine=engine)
    session.open(position)
    assert session.back() is None
    assert session.current_position is position
    assert session.history_count == 1

# =============================================================
# Session History Forward
# =============================================================

def test_forward_delegates_to_history_only(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.back()
    result=session.forward()
    assert result is next_position
    engine.move_next.assert_not_called()
    engine.move_previous.assert_not_called()

def test_forward_updates_position(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.back()
    session.forward()
    assert session.position is next_position
    assert session.current_position is next_position

def test_forward_returns_none_at_boundary(engine,position):
    session=ReaderSession(engine=engine)
    session.open(position)
    assert session.forward() is None
    assert session.position is position

# =============================================================
# History Branching
# =============================================================

def test_next_after_back_creates_new_history_branch(engine,position,next_position,another_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.back()
    engine.move_next.return_value=another_position
    session.next()
    assert session.position is another_position
    assert session.can_go_forward is False
    assert session.history.current is another_position

def test_previous_after_back_is_structural_not_history_navigation(engine,position,next_position,another_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.back()
    engine.move_previous.return_value=another_position
    result=session.previous()
    assert result is another_position
    engine.move_previous.assert_called_once_with(position)

# =============================================================
# Clear History
# =============================================================

def test_clear_history_delegates_to_history(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    assert session.history_count == 2
    session.clear_history()
    assert session.history_count == 0

def test_clear_history_does_not_clear_session_position(engine,position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.clear_history()
    assert session.position is position
    assert session.current_position is position
    assert session.has_position is True

def test_clear_history_disables_back_and_forward(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.back()
    session.clear_history()
    assert session.can_go_back is False
    assert session.can_go_forward is False

# =============================================================
# Display
# =============================================================

def test_display_name_without_position(engine):
    session=ReaderSession(engine=engine)
    assert session.display_name == "Reader Session"

def test_display_name_with_position(engine,position):
    session=ReaderSession(engine=engine,position=position)
    assert session.display_name == "Reader Session"

def test_display_text_without_position(engine):
    session=ReaderSession(engine=engine)
    assert session.display_text == "Reader Session"

def test_display_text_with_position(engine,position):
    session=ReaderSession(engine=engine,position=position)
    assert session.display_text == str(position)

def test_display_description_without_position(engine):
    session=ReaderSession(engine=engine)
    assert session.display_description == "Reader session without a current position."

def test_display_description_with_position(engine,position):
    session=ReaderSession(engine=engine,position=position)
    assert session.display_description == "Stateful Reader session with navigation history."

def test_string_representation_without_position(engine):
    session=ReaderSession(engine=engine)
    assert str(session) == "Reader Session"

def test_string_representation_with_position(engine,position):
    session=ReaderSession(engine=engine,position=position)
    assert str(session) == str(position)

# =============================================================
# State / History Consistency
# =============================================================

def test_next_then_back_restores_previous_position(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.return_value=next_position
    session.next()
    assert session.position is next_position
    assert session.back() is position
    assert session.position is position

def test_next_then_back_then_forward_restores_next_position(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    engine.move_next.return_value=next_position
    session.next()
    session.back()
    assert session.forward() is next_position
    assert session.position is next_position

def test_failed_next_preserves_history_state(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    session.history.record(next_position)
    session.back()
    assert session.can_go_forward is True
    engine.move_next.return_value=None
    session.next()
    assert session.position is position
    assert session.can_go_forward is True

def test_failed_previous_preserves_history_state(engine,position,next_position):
    session=ReaderSession(engine=engine,position=position)
    session.history.record(next_position)
    before=session.history_count
    engine.move_previous.return_value=None
    session.previous()
    assert session.position is position
    assert session.history_count == before

def test_history_count_reflects_session_history(engine,position,next_position,another_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    session.history.record(another_position)
    assert session.history_count == 3

def test_can_go_back_reflects_history(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    assert session.can_go_back is False
    session.history.record(next_position)
    assert session.can_go_back is True

def test_can_go_forward_reflects_history(engine,position,next_position):
    session=ReaderSession(engine=engine)
    session.open(position)
    session.history.record(next_position)
    assert session.can_go_forward is False
    session.back()
    assert session.can_go_forward is True

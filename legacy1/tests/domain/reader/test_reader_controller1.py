from __future__ import annotations
"""SanskritAI
==========
Reader Controller Unit Tests
"""
from unittest.mock import Mock
import pytest
from SanskritAI.domain.reader.reader_controller import ReaderController
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session import ReaderSession
@pytest.fixture
def engine():
    return Mock(spec=ReaderEngine)
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
def session(engine, position):
    value = Mock(spec=ReaderSession)
    value.engine = engine
    value.current_position = position
    value.has_position = True
    value.current_result = None
    value.has_result = False
    value.succeeded = False
    value.can_go_back = False
    value.can_go_forward = False
    value.history_count = 0
    value.display_text = str(position)
    return value
@pytest.fixture
def controller(session):
    return ReaderController(session=session)
def test_controller_stores_session(controller, session):
    assert controller.session is session
def test_controller_exposes_engine(controller, engine):
    assert controller.engine is engine
def test_controller_exposes_position(controller, position):
    assert controller.position is position
    assert controller.current_position is position
def test_controller_exposes_session_state(controller, session):
    assert controller.has_position is True
    assert controller.result is None
    assert controller.current_result is None
    assert controller.has_result is False
    assert controller.succeeded is False
    assert controller.can_go_back is False
    assert controller.can_go_forward is False
    assert controller.history_count == 0
def test_open_creates_controller_from_session(monkeypatch, engine, position):
    session = Mock(spec=ReaderSession)
    monkeypatch.setattr(
        ReaderSession,
        "open",
        Mock(return_value=session),
    )
    controller = ReaderController.open(engine, position)
    ReaderSession.open.assert_called_once_with(engine, position)
    assert controller.session is session
def test_open_position_delegates(controller, session, next_position):
    session.set_position.return_value = next_position
    assert controller.open_position(next_position) is next_position
    session.set_position.assert_called_once_with(next_position)
def test_set_position_delegates(controller, session, next_position):
    session.set_position.return_value = next_position
    assert controller.set_position(next_position) is next_position
    session.set_position.assert_called_once_with(next_position)
def test_set_position_none_delegates(controller, session):
    session.set_position.return_value = None
    assert controller.set_position(None) is None
    session.set_position.assert_called_once_with(None)
def test_resolve_delegates(controller, session):
    resolved = Mock()
    session.resolve.return_value = resolved
    assert controller.resolve() is resolved
    session.resolve.assert_called_once_with()
def test_next_delegates(controller, session, next_position):
    session.next.return_value = next_position
    assert controller.next() is next_position
    session.next.assert_called_once_with()
def test_previous_delegates(controller, session, next_position):
    session.previous.return_value = next_position
    assert controller.previous() is next_position
    session.previous.assert_called_once_with()
def test_back_delegates(controller, session, next_position):
    session.back.return_value = next_position
    assert controller.back() is next_position
    session.back.assert_called_once_with()
def test_forward_delegates(controller, session, next_position):
    session.forward.return_value = next_position
    assert controller.forward() is next_position
    session.forward.assert_called_once_with()
def test_move_next_delegates(controller, session):
    result = Mock(spec=ReaderSession)
    session.move_next.return_value = result
    assert controller.move_next() is result
    session.move_next.assert_called_once_with()
def test_move_previous_delegates(controller, session):
    result = Mock(spec=ReaderSession)
    session.move_previous.return_value = result
    assert controller.move_previous() is result
    session.move_previous.assert_called_once_with()
def test_clear_history_delegates(controller, session):
    controller.clear_history()
    session.clear_history.assert_called_once_with()
def test_document_delegates_to_engine(controller, engine):
    result = Mock()
    engine.document.return_value = result
    assert controller.document() is result
    engine.document.assert_called_once_with(None)
def test_document_with_id_delegates_to_engine(controller, engine):
    result = Mock()
    engine.document.return_value = result
    assert controller.document("document-1") is result
    engine.document.assert_called_once_with("document-1")
def test_chapter_delegates_to_engine(controller, engine):
    result = Mock()
    engine.chapter.return_value = result
    assert controller.chapter("chapter-1") is result
    engine.chapter.assert_called_once_with("chapter-1")
def test_sloka_delegates_to_engine(controller, engine):
    result = Mock()
    engine.sloka.return_value = result
    assert controller.sloka("sloka-1") is result
    engine.sloka.assert_called_once_with("sloka-1")
def test_word_delegates_to_engine(controller, engine):
    result = Mock()
    engine.word.return_value = result
    assert controller.word("word-1") is result
    engine.word.assert_called_once_with("word-1")
def test_resolve_position_delegates_to_engine(controller, engine, position):
    result = Mock()
    engine.resolve.return_value = result
    assert controller.resolve_position(position) is result
    engine.resolve.assert_called_once_with(position)
def test_controller_display_properties(controller):
    assert controller.display_name == "Reader Controller"
    assert controller.display_text == str(controller.position)
    assert "Application-facing controller" in controller.display_description
def test_controller_string_representation(controller):
    assert str(controller) == controller.display_text

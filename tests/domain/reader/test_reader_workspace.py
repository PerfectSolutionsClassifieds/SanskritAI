from __future__ import annotations

from unittest.mock import Mock

import pytest

from SanskritAI.domain.reader.reader_controller import ReaderController
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext
from SanskritAI.domain.reader.reader_session import ReaderSession
from SanskritAI.domain.reader.reader_workspace import ReaderWorkspace


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


@pytest.fixture
def workspace(controller):
    return ReaderWorkspace(controller=controller)


def test_workspace_stores_controller(workspace, controller):
    assert workspace.controller is controller


def test_workspace_exposes_session(workspace, session):
    assert workspace.session is session


def test_workspace_exposes_engine(workspace, engine):
    assert workspace.engine is engine


def test_workspace_exposes_position(workspace, position):
    assert workspace.position is position
    assert workspace.current_position is position


def test_workspace_exposes_result_state(workspace):
    assert workspace.result is None
    assert workspace.current_result is None
    assert workspace.has_result is False
    assert workspace.succeeded is False


def test_workspace_exposes_navigation_state(workspace):
    assert workspace.can_go_back is False
    assert workspace.can_go_forward is False
    assert workspace.history_count == 0


def test_workspace_exposes_position_state(workspace):
    assert workspace.has_position is True


def test_workspace_derives_selection_from_current_position(workspace, position):
    selection = workspace.selection
    assert isinstance(selection, ReaderSelectionContext)
    assert selection.position is position


def test_workspace_selection_is_derived_from_current_position(workspace, session):
    first_position = session.current_position
    first_selection = workspace.selection

    second_position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )
    session.current_position = second_position

    assert first_selection.position is first_position
    assert workspace.selection.position is second_position
    assert workspace.selection is not first_selection


def test_workspace_selection_is_none_without_position(controller, session):
    session.current_position = None
    session.has_position = False

    workspace = ReaderWorkspace(controller=controller)

    assert workspace.position is None
    assert workspace.current_position is None
    assert workspace.selection is None
    assert workspace.has_position is False


def test_workspace_open_creates_controller(monkeypatch, engine, position):
    controller = Mock(spec=ReaderController)

    monkeypatch.setattr(
        ReaderController,
        "open",
        Mock(return_value=controller),
    )

    workspace = ReaderWorkspace.open(engine, position)

    ReaderController.open.assert_called_once_with(engine, position)
    assert workspace.controller is controller


def test_workspace_display_contract(workspace, position):
    assert workspace.display_name == "Reader Workspace"
    assert workspace.display_text == str(position)
    assert "Application-level workspace" in workspace.display_description


def test_workspace_string_representation(workspace):
    assert str(workspace) == workspace.display_text


def test_workspace_does_not_duplicate_controller_state(workspace, session):
    assert workspace.position is session.current_position
    assert workspace.result is session.current_result
    assert workspace.has_position is session.has_position
    assert workspace.has_result is session.has_result
    assert workspace.succeeded is session.succeeded
    assert workspace.can_go_back is session.can_go_back
    assert workspace.can_go_forward is session.can_go_forward
    assert workspace.history_count is session.history_count

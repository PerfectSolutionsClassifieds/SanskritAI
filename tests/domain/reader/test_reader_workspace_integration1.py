from __future__ import annotations

from SanskritAI.domain.reader.reader_controller import ReaderController
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext
from SanskritAI.domain.reader.reader_workspace import ReaderWorkspace


def test_workspace_open_integrates_with_reader_controller(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    assert isinstance(workspace, ReaderWorkspace)
    assert isinstance(workspace.controller, ReaderController)
    assert workspace.engine is reader_engine
    assert workspace.position == reader_position


def test_workspace_exposes_active_reader_session(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    assert workspace.session is workspace.controller.session
    assert workspace.engine is workspace.session.engine


def test_workspace_exposes_resolved_reader_state(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    assert workspace.has_position is True
    assert workspace.current_position == reader_position
    assert workspace.selection is not None
    assert isinstance(workspace.selection, ReaderSelectionContext)


def test_workspace_selection_tracks_session_position(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    initial_selection = workspace.selection

    workspace.controller.next()

    assert workspace.current_position is workspace.session.current_position

    if workspace.current_position is not None:
        assert workspace.selection is not initial_selection
        assert workspace.selection.position is workspace.current_position


def test_workspace_preserves_controller_navigation_semantics(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    initial_position = workspace.current_position

    workspace.controller.next()

    assert workspace.current_position is workspace.controller.current_position
    assert workspace.current_position != initial_position

    workspace.controller.previous()

    assert workspace.current_position is workspace.controller.current_position
    assert workspace.current_position == initial_position


def test_workspace_preserves_browser_history_semantics(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    initial_position = workspace.current_position

    workspace.controller.next()

    next_position = workspace.current_position

    assert next_position != initial_position
    assert workspace.can_go_back is True

    workspace.controller.back()

    assert workspace.current_position == initial_position

    if next_position is not None:
        assert workspace.can_go_forward is True

    workspace.controller.forward()

    assert workspace.current_position == next_position


def test_workspace_state_remains_controller_owned(
    reader_engine: ReaderEngine,
    reader_position: ReaderPosition,
):
    workspace = ReaderWorkspace.open(
        reader_engine,
        reader_position,
    )

    assert workspace.position is workspace.controller.current_position
    assert workspace.result is workspace.controller.current_result
    assert workspace.has_position == workspace.controller.has_position
    assert workspace.has_result == workspace.controller.has_result
    assert workspace.succeeded == workspace.controller.succeeded
    assert workspace.can_go_back == workspace.controller.can_go_back
    assert workspace.can_go_forward == workspace.controller.can_go_forward

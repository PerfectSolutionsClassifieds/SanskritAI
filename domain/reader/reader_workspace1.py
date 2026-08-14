from __future__ import annotations

"""
SanskritAI
==========

Reader Workspace

Application-level working environment for an active ReaderController.

ReaderWorkspace coordinates access to the active ReaderController without
duplicating navigation, resolution, session, or history state.

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.domain.reader.reader_controller import ReaderController
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session import ReaderSession
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext


@dataclass(slots=True)
class ReaderWorkspace:
    """
    Application-level workspace for an active ReaderController.

    ReaderWorkspace does not own an independent ReaderPosition,
    ReaderResult, navigation history, or resolution state. These remain
    owned by ReaderController and its underlying ReaderSession.
    """

    controller: ReaderController

    @classmethod
    def open(
        cls,
        engine: ReaderEngine,
        position: ReaderPosition,
    ) -> "ReaderWorkspace":
        """Create a workspace with a newly opened ReaderController."""
        return cls(
            controller=ReaderController.open(
                engine,
                position,
            )
        )

    @property
    def session(self) -> ReaderSession:
        """Return the active ReaderSession."""
        return self.controller.session

    @property
    def engine(self) -> ReaderEngine:
        """Return the ReaderEngine used by the active session."""
        return self.controller.engine

    @property
    def position(self) -> ReaderPosition | None:
        """Return the current ReaderPosition."""
        return self.controller.current_position

    @property
    def current_position(self) -> ReaderPosition | None:
        """Return the current ReaderPosition."""
        return self.controller.current_position

    @property
    def selection(self) -> ReaderSelectionContext | None:
        """
        Return the immutable selection context for the current position.

        The selection is derived from the controller's canonical position
        and is never maintained as duplicate workspace state.
        """
        position = self.controller.current_position
        if position is None:
            return None
        return ReaderSelectionContext.from_position(position)

    @property
    def result(self) -> Any:
        """Return the current ReaderResult, if available."""
        return self.controller.current_result

    @property
    def current_result(self) -> Any:
        """Return the current ReaderResult, if available."""
        return self.controller.current_result

    @property
    def has_position(self) -> bool:
        """Return True when a current ReaderPosition exists."""
        return self.controller.has_position

    @property
    def has_result(self) -> bool:
        """Return True when a ReaderResult is available."""
        return self.controller.has_result

    @property
    def succeeded(self) -> bool:
        """Return the success state of the current ReaderResult."""
        return self.controller.succeeded

    @property
    def can_go_back(self) -> bool:
        """Return whether browser-style back navigation is available."""
        return self.controller.can_go_back

    @property
    def can_go_forward(self) -> bool:
        """Return whether browser-style forward navigation is available."""
        return self.controller.can_go_forward

    @property
    def history_count(self) -> int:
        """Return the controller-visible history count."""
        return self.controller.history_count

    @property
    def display_name(self) -> str:
        """Return the workspace display name."""
        return "Reader Workspace"

    @property
    def display_text(self) -> str:
        """Return the current Reader display text."""
        return self.controller.display_text

    @property
    def display_description(self) -> str:
        """Return the workspace display description."""
        return "Application-level workspace for the active Reader controller."

    def __str__(self) -> str:
        return self.display_text

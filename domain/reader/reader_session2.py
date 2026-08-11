from __future__ import annotations

"""
SanskritAI
==========

Reader Session
==============

Stateful reader-session façade built on top of:

    ReaderEngine
        │
        ▼
    ReaderSessionHistory

Responsibilities
----------------
ReaderSession owns the user's current reading position and
coordinates navigation with ReaderSessionHistory.

ReaderEngine remains responsible for structural navigation.

ReaderSessionHistory remains responsible for session history.

This separation is intentional:

    ReaderEngine
        = corpus navigation

    ReaderSessionHistory
        = browsing history

    ReaderSession
        = user-facing session state

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_session_history import (
    ReaderSessionHistory,
)


@dataclass(
    slots=True,
)
class ReaderSession:
    """
    Stateful reader session.

    The session does not replace ReaderEngine navigation.

    Instead:

        next / previous
            -> ReaderEngine

        back / forward
            -> ReaderSessionHistory
    """

    engine: ReaderEngine

    history: ReaderSessionHistory = field(
        default_factory=ReaderSessionHistory,
    )

    position: ReaderPosition | None = None

    # =========================================================
    # Session State
    # =========================================================

    @property
    def current_position(
        self,
    ) -> ReaderPosition | None:
        """
        Return the current reader position.
        """

        return self.position

    @property
    def has_position(
        self,
    ) -> bool:
        """
        Return True when the session has a current position.
        """

        return self.position is not None

    # =========================================================
    # History Exposure
    # =========================================================

    @property
    def can_go_back(
        self,
    ) -> bool:
        """
        Return whether session history has a previous position.
        """

        return self.history.can_go_back

    @property
    def can_go_forward(
        self,
    ) -> bool:
        """
        Return whether session history has a forward position.
        """

        return self.history.can_go_forward

    @property
    def history_count(
        self,
    ) -> int:
        """
        Return the number of positions represented by history.
        """

        return self.history.count

    # =========================================================
    # Position Management
    # =========================================================

    def set_position(
        self,
        position: ReaderPosition | None,
    ) -> ReaderPosition | None:
        """
        Establish a new session position.

        A new explicit position represents a new browsing root,
        therefore existing session history is cleared.
        """

        self.position = position

        self.history.clear()

        if position is not None:
            self.history.push(
                position,
            )

        return self.position

    # =========================================================
    # Forward Navigation
    # =========================================================

    def next(
        self,
    ) -> ReaderPosition | None:
        """
        Navigate forward through the ReaderEngine.

        Successful navigation records the resulting position
        in ReaderSessionHistory.
        """

        if self.position is None:
            return None

        result = self.engine.move_next(
            self.position,
        )

        if result is None:
            return None

        self.position = result

        self.history.push(
            result,
        )

        return result

    # ---------------------------------------------------------

    def previous(
        self,
    ) -> ReaderPosition | None:
        """
        Navigate backward structurally through ReaderEngine.

        This is NOT session-history back navigation.

        It asks ReaderEngine for the previous object at the
        current structural level.
        """

        if self.position is None:
            return None

        result = self.engine.move_previous(
            self.position,
        )

        if result is None:
            return None

        self.position = result

        self.history.push(
            result,
        )

        return result

    # =========================================================
    # Session History Navigation
    # =========================================================

    def back(
        self,
    ) -> ReaderPosition | None:
        """
        Move backward through browsing history.

        This operation does not invoke ReaderEngine navigation.
        """

        result = self.history.back()

        if result is None:
            return None

        self.position = result

        return result

    # ---------------------------------------------------------

    def forward(
        self,
    ) -> ReaderPosition | None:
        """
        Move forward through browsing history.

        This operation does not invoke ReaderEngine navigation.
        """

        result = self.history.forward()

        if result is None:
            return None

        self.position = result

        return result

    # =========================================================
    # History Control
    # =========================================================

    def clear_history(
        self,
    ) -> None:
        """
        Clear session history.
        """

        self.history.clear()

    # =========================================================
    # Display
    # =========================================================

    @property
    def display_name(
        self,
    ) -> str:
        return "Reader Session"

    @property
    def display_text(
        self,
    ) -> str:
        if self.position is None:
            return "Reader Session"

        return str(
            self.position,
        )

    @property
    def display_description(
        self,
    ) -> str:
        if self.position is None:
            return (
                "Reader session without a current position."
            )

        return (
            "Stateful Reader session with navigation history."
        )

    # =========================================================

    def __str__(
        self,
    ) -> str:
        return self.display_text

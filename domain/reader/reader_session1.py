from __future__ import annotations

"""
SanskritAI
==========

ReaderSession

Purpose
-------
Represents the active reading session of the SanskritAI Reader
Domain.

ReaderSession is intentionally a thin stateful layer above
ReaderEngine.

Responsibilities
----------------
* maintain the current ReaderPosition
* maintain the current ReaderResult
* resolve the current position
* move forward
* move backward
* preserve reader state after navigation

Architecture
------------

Corpus
   │
   ▼
DefaultReaderRepository
   │
   ▼
ReaderNavigator
   │
   ▼
ReaderEngine
   │
   ▼
ReaderSession
   │
   ▼
ReaderResult

Design Principle
----------------
ReaderSession owns reader state.

It does NOT:
* construct Corpus objects
* perform repository lookups directly
* implement navigation algorithms
* perform Sanskrit linguistic analysis

Those responsibilities remain below the session layer.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, replace

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_result import (
    ReaderResult,
)


@dataclass(frozen=True, slots=True)
class ReaderSession:
    """
    Active state of a SanskritAI Reader session.

    A session consists of:

        ReaderEngine
            +
        current ReaderPosition
            +
        current ReaderResult
    """

    engine: ReaderEngine
    position: ReaderPosition
    result: ReaderResult

    # =========================================================
    # Construction
    # =========================================================

    @classmethod
    def open(
        cls,
        engine: ReaderEngine,
        position: ReaderPosition,
    ) -> "ReaderSession":
        """
        Open a new reader session at the supplied position.

        The position is immediately resolved through ReaderEngine.
        """

        result = engine.resolve(
            position,
        )

        return cls(
            engine=engine,
            position=position,
            result=result,
        )

    # =========================================================
    # Current State
    # =========================================================

    @property
    def current_position(
        self,
    ) -> ReaderPosition:
        """
        Return the current reader position.
        """

        return self.position

    @property
    def current_result(
        self,
    ) -> ReaderResult:
        """
        Return the current ReaderResult.
        """

        return self.result

    # =========================================================
    # Resolution
    # =========================================================

    def resolve(
        self,
    ) -> ReaderResult:
        """
        Re-resolve the current position.

        The returned result becomes the session's current result.
        """

        result = self.engine.resolve(
            self.position,
        )

        return replace(
            self,
            result=result,
        )

    # =========================================================
    # Navigation
    # =========================================================

    def move_next(
        self,
    ) -> "ReaderSession | None":
        """
        Move to the next reader position.

        Returns
        -------
        ReaderSession | None
            A new session at the next position.

        None is returned when the current position is at the
        navigation boundary.
        """

        next_position = self.engine.move_next(
            self.position,
        )

        if next_position is None:
            return None

        return self.open(
            engine=self.engine,
            position=next_position,
        )

    def move_previous(
        self,
    ) -> "ReaderSession | None":
        """
        Move to the previous reader position.

        Returns
        -------
        ReaderSession | None
            A new session at the previous position.

        None is returned when the current position is at the
        navigation boundary.
        """

        previous_position = self.engine.move_previous(
            self.position,
        )

        if previous_position is None:
            return None

        return self.open(
            engine=self.engine,
            position=previous_position,
        )

    # =========================================================
    # Convenience
    # =========================================================

    @property
    def has_result(
        self,
    ) -> bool:
        """
        Whether the session currently has a ReaderResult.
        """

        return self.result is not None

    @property
    def succeeded(
        self,
    ) -> bool:
        """
        Whether the current ReaderResult represents success.
        """

        return self.result.succeeded

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
        return self.result.display_text

    @property
    def display_description(
        self,
    ) -> str:
        return (
            f"Reader session at "
            f"{self.position}"
        )

    # =========================================================

    def __str__(
        self,
    ) -> str:
        return self.display_text

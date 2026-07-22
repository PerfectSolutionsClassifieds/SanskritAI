from __future__ import annotations

"""
SanskritAI
==========

Cursor State

Immutable runtime state of a ParserCursor.

CursorState captures the current navigation position within a
TokenStream. Unlike CursorMark, which is an explicit checkpoint,
CursorState represents the parser's current position at any
moment.

Version
-------
v0.6.0
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CursorState:
    """
    Immutable parser cursor state.
    """

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    index: int = 0

    # ---------------------------------------------------------
    # Parsing status
    # ---------------------------------------------------------

    eof: bool = False

    error: bool = False

    # ---------------------------------------------------------
    # Convenience properties
    # ---------------------------------------------------------

    @property
    def is_valid(self) -> bool:
        """
        Returns True if the cursor is not in an error state.
        """
        return not self.error

    @property
    def can_advance(self) -> bool:
        """
        Returns True if the cursor can advance.
        """
        return not self.eof and not self.error

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if parsing has reached a terminal state.
        """
        return self.eof or self.error

    # ---------------------------------------------------------
    # State transitions
    # ---------------------------------------------------------

    def advance(self, step: int = 1) -> "CursorState":
        """
        Return a new state advanced by the specified number of
        positions.
        """
        return CursorState(
            index=self.index + step,
            eof=self.eof,
            error=self.error,
        )

    def with_eof(self) -> "CursorState":
        """
        Return a new state marked as end-of-stream.
        """
        return CursorState(
            index=self.index,
            eof=True,
            error=self.error,
        )

    def with_error(self) -> "CursorState":
        """
        Return a new state marked as erroneous.
        """
        return CursorState(
            index=self.index,
            eof=self.eof,
            error=True,
        )

    def reset(self) -> "CursorState":
        """
        Return the initial cursor state.
        """
        return CursorState()

    def __str__(self) -> str:
        flags = []

        if self.eof:
            flags.append("EOF")

        if self.error:
            flags.append("ERROR")

        suffix = f" [{' | '.join(flags)}]" if flags else ""

        return f"CursorState(index={self.index}){suffix}"

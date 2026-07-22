from __future__ import annotations

"""
SanskritAI
==========

Cursor Exception

Base exception for the Parser Cursor subsystem.

All parser cursor and navigation related exceptions should
derive from CursorException.

This establishes a dedicated exception hierarchy for parser
navigation while remaining independent of parsing grammar,
validation and semantic analysis.

Version
-------
v0.6.0
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CursorException(Exception):
    """
    Base exception raised by the Parser Cursor subsystem.
    """

    # ---------------------------------------------------------
    # Exception information
    # ---------------------------------------------------------

    message: str

    index: int | None = None

    # ---------------------------------------------------------
    # Exception API
    # ---------------------------------------------------------

    def __str__(self) -> str:
        """
        Human-readable exception message.
        """
        if self.index is None:
            return self.message

        return (
            f"{self.message} "
            f"(cursor index={self.index})"
        )

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """
        return (
            "CursorException("
            f"message={self.message!r}, "
            f"index={self.index!r})"
        )

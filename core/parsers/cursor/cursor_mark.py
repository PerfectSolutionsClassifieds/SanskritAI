from __future__ import annotations

"""
SanskritAI
==========

Cursor Mark

Immutable checkpoint used by ParserCursor.

A CursorMark stores enough information to restore a parser
cursor to a previous location during recursive-descent parsing
or speculative parsing.

Version
-------
v0.6.0
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CursorMark:
    """
    Immutable parser cursor checkpoint.
    """

    # ---------------------------------------------------------
    # Cursor position
    # ---------------------------------------------------------

    index: int

    # ---------------------------------------------------------
    # Optional descriptive label
    # ---------------------------------------------------------

    label: str = ""

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_named(self) -> bool:
        """
        Returns True if this mark has a descriptive label.
        """
        return bool(self.label)

    def __str__(self) -> str:
        if self.label:
            return f"{self.label}@{self.index}"
        return f"@{self.index}"

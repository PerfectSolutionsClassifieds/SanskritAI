from __future__ import annotations

"""
SanskritAI
==========

Token Position

Immutable source location metadata associated with a
TokenizerToken.

TokenPosition is intentionally language-agnostic and may be
used throughout the SanskritAI processing pipeline for
diagnostics, parsing and analysis.

Version
-------
v0.6.0
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenPosition:
    """
    Immutable position of a tokenizer token within a source.
    """

    # ---------------------------------------------------------
    # Absolute character offsets
    # ---------------------------------------------------------

    start_offset: int

    end_offset: int

    # ---------------------------------------------------------
    # Human-readable location
    # ---------------------------------------------------------

    line: int = 1

    column: int = 1

    # ---------------------------------------------------------
    # Derived properties
    # ---------------------------------------------------------

    @property
    def length(self) -> int:
        """
        Length of the token in characters.
        """
        return max(0, self.end_offset - self.start_offset)

    @property
    def is_valid(self) -> bool:
        """
        Returns True if the position represents a valid span.
        """
        return (
            self.start_offset >= 0
            and self.end_offset >= self.start_offset
            and self.line >= 1
            and self.column >= 1
        )

    def shift(
        self,
        *,
        offset: int = 0,
        line: int = 0,
        column: int = 0,
    ) -> "TokenPosition":
        """
        Return a new TokenPosition shifted by the supplied
        values.
        """
        return TokenPosition(
            start_offset=self.start_offset + offset,
            end_offset=self.end_offset + offset,
            line=self.line + line,
            column=self.column + column,
        )

    def __str__(self) -> str:
        """
        Human-readable representation.
        """
        return (
            f"line={self.line}, "
            f"column={self.column}, "
            f"offset={self.start_offset}:{self.end_offset}"
        )

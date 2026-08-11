from __future__ import annotations

"""
SanskritAI
==========

Sloka Position

Immutable navigation cursor representing a śloka.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SlokaPosition(
    ReaderPosition,
):
    """
    Immutable śloka navigation cursor.
    """

    chapter_index: int = 0
    sloka_index: int = 0
    word_index: int = -1

    def __post_init__(self) -> None:
        object.__setattr__(self, "word_index", -1)

    @property
    def display_name(self) -> str:
        return "Sloka Position"

    @property
    def display_text(self) -> str:
        return (
            f"Chapter {self.chapter_index + 1}, "
            f"Śloka {self.sloka_index + 1}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable navigation cursor for a śloka."
        )

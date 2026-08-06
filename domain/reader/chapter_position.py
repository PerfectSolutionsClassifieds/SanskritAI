from __future__ import annotations

"""
SanskritAI
==========

Chapter Position

Immutable navigation cursor representing a chapter.

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
class ChapterPosition(
    ReaderPosition,
):
    """
    Immutable chapter navigation cursor.
    """

    chapter_index: int = 0
    sloka_index: int = 0
    word_index: int = -1

    def __post_init__(self) -> None:
        object.__setattr__(self, "sloka_index", 0)
        object.__setattr__(self, "word_index", -1)

    @property
    def display_name(self) -> str:
        return "Chapter Position"

    @property
    def display_text(self) -> str:
        return (
            f"Chapter {self.chapter_index + 1}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable navigation cursor for a chapter."
        )

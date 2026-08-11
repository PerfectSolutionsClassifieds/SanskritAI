from __future__ import annotations

"""
SanskritAI
==========

Word Position

Immutable navigation cursor representing a word within a śloka.

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
class WordPosition(
    ReaderPosition,
):
    """
    Immutable word navigation cursor.
    """

    chapter_index: int = 0
    sloka_index: int = 0
    word_index: int = 0

    @property
    def display_name(self) -> str:
        return "Word Position"

    @property
    def display_text(self) -> str:
        return (
            f"Chapter {self.chapter_index + 1}, "
            f"Śloka {self.sloka_index + 1}, "
            f"Word {self.word_index + 1}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable navigation cursor for a word."
        )

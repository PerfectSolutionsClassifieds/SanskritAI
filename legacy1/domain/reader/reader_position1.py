from __future__ import annotations

"""
SanskritAI
==========

Reader Position

Canonical immutable navigation cursor for the Reader Domain.

ReaderPosition identifies a precise location within a
ReaderDocument.

Hierarchy
---------

ReaderDocument
    └── Chapter
          └── Śloka
                └── Word

Every specialized navigation position derives from this
canonical value object.

Future Extensions
-----------------

• bookmarks

• browser history

• deep links

• citations

• annotations

• AI navigation

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import (
    ValueObject,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderPosition(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable reader position.
    """

    chapter_index: int = 0

    sloka_index: int = 0

    word_index: int = -1

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Position"

    @property
    def display_text(self) -> str:

        if self.word_index >= 0:
            return (
                f"Chapter {self.chapter_index + 1}, "
                f"Śloka {self.sloka_index + 1}, "
                f"Word {self.word_index + 1}"
            )

        return (
            f"Chapter {self.chapter_index + 1}, "
            f"Śloka {self.sloka_index + 1}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable navigation cursor within a "
            "ReaderDocument."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_chapter_position(self) -> bool:
        return (
            self.sloka_index == 0
            and self.word_index < 0
        )

    @property
    def is_sloka_position(self) -> bool:
        return self.word_index < 0

    @property
    def is_word_position(self) -> bool:
        return self.word_index >= 0

    # ---------------------------------------------------------
    # Builders
    # ---------------------------------------------------------

    def with_chapter(
        self,
        chapter_index: int,
    ) -> "ReaderPosition":

        return ReaderPosition(
            chapter_index=chapter_index,
            sloka_index=0,
            word_index=-1,
        )

    def with_sloka(
        self,
        sloka_index: int,
    ) -> "ReaderPosition":

        return ReaderPosition(
            chapter_index=self.chapter_index,
            sloka_index=sloka_index,
            word_index=-1,
        )

    def with_word(
        self,
        word_index: int,
    ) -> "ReaderPosition":

        return ReaderPosition(
            chapter_index=self.chapter_index,
            sloka_index=self.sloka_index,
            word_index=word_index,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

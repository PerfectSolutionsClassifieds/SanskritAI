from __future__ import annotations

"""
SanskritAI
==========

Reader Position

Canonical immutable navigation and citation object.

Rather than storing transient UI indices, ReaderPosition stores
stable canonical identifiers that uniquely identify a location
within the SanskritAI corpus.

Hierarchy

Corpus
    └── Purāṇa
          └── Chapter
                └── Śloka
                      └── Word

This object becomes the universal navigation cursor used by

    • Reader Engine
    • Reader UI
    • Resolution Pipeline
    • AI / RAG
    • Search
    • Annotation
    • Bookmarking
    • Commentary
    • Cross References

Version
-------
v2.0.0
"""

from dataclasses import dataclass
from typing import Optional

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


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
    Canonical immutable corpus position.
    """

    corpus_id: str

    purana_id: str

    chapter_id: str

    sloka_id: Optional[str] = None

    word_id: Optional[str] = None

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Position"

    @property
    def display_text(self) -> str:

        if self.word_id is not None:
            return (
                f"{self.purana_id} → "
                f"{self.chapter_id} → "
                f"{self.sloka_id} → "
                f"{self.word_id}"
            )

        if self.sloka_id is not None:
            return (
                f"{self.purana_id} → "
                f"{self.chapter_id} → "
                f"{self.sloka_id}"
            )

        return (
            f"{self.purana_id} → "
            f"{self.chapter_id}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Canonical immutable corpus position."
        )

    # ---------------------------------------------------------
    # Position Type
    # ---------------------------------------------------------

    @property
    def is_chapter_position(self) -> bool:
        return self.sloka_id is None

    @property
    def is_sloka_position(self) -> bool:
        return (
            self.sloka_id is not None
            and self.word_id is None
        )

    @property
    def is_word_position(self) -> bool:
        return self.word_id is not None

    # ---------------------------------------------------------
    # Builders
    # ---------------------------------------------------------

    def with_sloka(
        self,
        sloka_id: str,
    ) -> "ReaderPosition":

        return ReaderPosition(
            corpus_id=self.corpus_id,
            purana_id=self.purana_id,
            chapter_id=self.chapter_id,
            sloka_id=sloka_id,
        )

    def with_word(
        self,
        word_id: str,
    ) -> "ReaderPosition":

        return ReaderPosition(
            corpus_id=self.corpus_id,
            purana_id=self.purana_id,
            chapter_id=self.chapter_id,
            sloka_id=self.sloka_id,
            word_id=word_id,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

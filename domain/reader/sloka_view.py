from __future__ import annotations

"""
SanskritAI
==========

Sloka View

Immutable reader representation of a canonical śloka.

Hierarchy

ReaderDocument
    └── ChapterView
            └── SlokaView
                    └── WordView

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.reader.reader_view import (
    ReaderView,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.word_view import (
    WordView,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SlokaView(
    ReaderView,
):
    """
    Immutable Reader representation of a śloka.
    """

    words: tuple[
        WordView,
        ...
    ] = field(
        default_factory=tuple,
    )

    sloka_text: str = ""

    translation: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Śloka"

    @property
    def display_text(self) -> str:

        if self.sloka_text:
            return self.sloka_text

        return super().display_text

    @property
    def display_description(self) -> str:
        return (
            "Immutable reader śloka."
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def word_count(self) -> int:
        return len(self.words)

    @property
    def is_empty(self) -> bool:
        return self.word_count == 0

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def word(
        self,
        word_id: str,
    ) -> WordView:
        """
        Returns a word by canonical identifier.
        """

        for word in self.words:

            if word.identifier == word_id:
                return word

        raise KeyError(
            f"Unknown word '{word_id}'."
        )

    def contains(
        self,
        position: ReaderPosition,
    ) -> bool:
        """
        Determines whether a reader position belongs
        to this śloka.
        """

        if position.sloka_id != self.identifier:
            return False

        if position.word_id is None:
            return True

        return (
            position.word_id
            in {
                word.identifier
                for word in self.words
            }
        )

    # ---------------------------------------------------------

    def __iter__(self):
        return iter(self.words)

    def __len__(self):
        return self.word_count

    def __getitem__(
        self,
        index: int,
    ) -> WordView:
        return self.words[index]

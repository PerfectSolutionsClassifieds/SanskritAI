from __future__ import annotations

"""
SanskritAI
==========

Chapter View

Immutable reader representation of one canonical chapter.

Hierarchy

ReaderDocument
    └── ChapterView
            └── SlokaView

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

from SanskritAI.domain.reader.sloka_view import (
    SlokaView,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ChapterView(
    ReaderView,
):
    """
    Immutable Reader representation of a chapter.
    """

    slokas: tuple[
        SlokaView,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Chapter"

    @property
    def display_description(self) -> str:
        return (
            "Immutable reader chapter."
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def sloka_count(
        self,
    ) -> int:
        return len(
            self.slokas,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.sloka_count == 0

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def sloka(
        self,
        sloka_id: str,
    ) -> SlokaView:
        """
        Returns a śloka by canonical identifier.
        """

        for sloka in self.slokas:

            if sloka.identifier == sloka_id:
                return sloka

        raise KeyError(
            f"Unknown śloka '{sloka_id}'."
        )

    def contains(
        self,
        position: ReaderPosition,
    ) -> bool:
        """
        Determines whether a canonical reader position belongs
        to this chapter.
        """

        if position.chapter_id != self.identifier:
            return False

        if position.sloka_id is None:
            return True

        return (
            position.sloka_id
            in {
                sloka.identifier
                for sloka in self.slokas
            }
        )

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(
        self,
    ):
        return iter(
            self.slokas,
        )

    def __len__(
        self,
    ) -> int:
        return self.sloka_count

    def __getitem__(
        self,
        index: int,
    ) -> SlokaView:
        return self.slokas[index]

from __future__ import annotations

"""
SanskritAI
==========

Reader Document

Aggregate Root of the Reader Domain.

A ReaderDocument represents one canonical document exposed to
the Reader Layer.

The document owns an immutable hierarchy of ChapterView
objects and provides efficient lookup by canonical identifiers.

Hierarchy
---------

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

from SanskritAI.domain.reader.chapter_view import (
    ChapterView,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderDocument(
    ReaderView,
):
    """
    Aggregate root of the Reader Domain.
    """

    chapters: tuple[
        ChapterView,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Document"

    @property
    def display_description(self) -> str:
        return (
            "Immutable reader document."
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    @property
    def chapter_count(
        self,
    ) -> int:
        return len(
            self.chapters,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return (
            self.chapter_count == 0
        )

    def chapter(
        self,
        chapter_id: str,
    ) -> ChapterView:
        """
        Returns a chapter by canonical identifier.
        """

        for chapter in self.chapters:

            if chapter.identifier == chapter_id:
                return chapter

        raise KeyError(
            f"Unknown chapter '{chapter_id}'."
        )

    def contains(
        self,
        position: ReaderPosition,
    ) -> bool:
        """
        Determines whether a canonical reader position belongs
        to this document.
        """

        return (
            position.chapter_id
            in {
                chapter.identifier
                for chapter in self.chapters
            }
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):
        return iter(
            self.chapters,
        )

    def __len__(
        self,
    ) -> int:
        return self.chapter_count

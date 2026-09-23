from __future__ import annotations

"""
SanskritAI
==========

Chapter View

Represents one canonical chapter inside a ReaderDocument.

Hierarchy
---------

ReaderDocument
    │
    └── ChapterView
            │
            └── SlokaView

Purpose
-------

ChapterView is a Reader-layer object.

It represents one chapter exactly as presented to the user.

It owns ordered references to SlokaView objects but performs
no linguistic analysis.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.reader.reader_node import ReaderNode


@dataclass(frozen=True, slots=True)
class ChapterView(ReaderNode):
    """
    Immutable reader representation of a chapter.
    """

    document_identifier: str = ""

    chapter_number: int = 0

    chapter_title: str = ""

    section_title: str = ""

    sloka_count: int = 0

    opening_page: int | None = None

    closing_page: int | None = None

    source_reference: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    notes: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        if self.chapter_title:
            return (
                f"Chapter {self.chapter_number}: "
                f"{self.chapter_title}"
            )

        return f"Chapter {self.chapter_number}"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.notes

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_section_title(self) -> bool:
        return bool(self.section_title)

    @property
    def has_source_reference(self) -> bool:
        return bool(self.source_reference)

    @property
    def has_page_information(self) -> bool:
        return (
            self.opening_page is not None
            and self.closing_page is not None
        )

    @property
    def first_sloka_identifier(self) -> str | None:
        if not self.children:
            return None
        return self.children[0]

    @property
    def last_sloka_identifier(self) -> str | None:
        if not self.children:
            return None
        return self.children[-1]

    @property
    def is_empty(self) -> bool:
        return self.sloka_count == 0

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

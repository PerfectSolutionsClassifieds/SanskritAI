from __future__ import annotations

"""
SanskritAI
==========

Reader Document

Represents a complete canonical document within the Reader
Domain.

Examples
--------

• Brahma Purāṇa

• Śiva Purāṇa

• Viṣṇu Purāṇa

• Bhagavad Gītā

• Ṛgveda

Hierarchy
---------

ReaderNode
    │
    └── ReaderDocument
            │
            └── ChapterView

The ReaderDocument is the root aggregate exposed to the
Reader UI.

It owns the ordered collection of ChapterView objects while
remaining independent of the linguistic analysis kernels.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.reader.reader_node import ReaderNode


@dataclass(frozen=True, slots=True)
class ReaderDocument(
    ReaderNode,
):
    """
    Immutable reader representation of a canonical document.
    """

    document_title: str = ""

    canonical_name: str = ""

    abbreviation: str = ""

    document_type: str = ""

    language: str = "Sanskrit"

    script: str = "Devanagari"

    edition: str = ""

    publisher: str = ""

    volume: str = ""

    chapter_count: int = 0

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
        if self.document_title:
            return self.document_title

        if self.canonical_name:
            return self.canonical_name

        return "Reader Document"

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
    def has_chapters(self) -> bool:
        return len(self.children) > 0

    @property
    def first_chapter_identifier(self) -> str | None:
        if not self.children:
            return None

        return self.children[0]

    @property
    def last_chapter_identifier(self) -> str | None:
        if not self.children:
            return None

        return self.children[-1]

    @property
    def has_source_reference(self) -> bool:
        return bool(self.source_reference)

    @property
    def has_edition(self) -> bool:
        return bool(self.edition)

    @property
    def has_publisher(self) -> bool:
        return bool(self.publisher)

    @property
    def is_empty(self) -> bool:
        return self.chapter_count == 0

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

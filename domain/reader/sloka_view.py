from __future__ import annotations

"""
SanskritAI
==========

Sloka View

Represents one canonical Sanskrit śloka inside the Reader
Domain.

Hierarchy
---------

ReaderDocument
        │
        ▼
ChapterView
        │
        ▼
SlokaView
        │
        ▼
WordView

A SlokaView owns the ordered collection of WordView objects.

It contains no linguistic reasoning. All linguistic analysis
is delegated to ResolutionResult attached to individual words.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.reader.reader_node import ReaderNode


@dataclass(frozen=True, slots=True)
class SlokaView(
    ReaderNode,
):
    """
    Immutable reader representation of a Sanskrit śloka.
    """

    document_identifier: str = ""

    chapter_identifier: str = ""

    chapter_number: int = 0

    sloka_number: int = 0

    canonical_text: str = ""

    devanagari_text: str = ""

    transliteration: str = ""

    translation: str = ""

    context: str = ""

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
        return (
            f"Śloka {self.sloka_number}"
        )

    @property
    def display_text(self) -> str:
        if self.devanagari_text:
            return self.devanagari_text

        if self.canonical_text:
            return self.canonical_text

        return self.display_name

    @property
    def display_description(self) -> str:
        return self.translation

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_translation(self) -> bool:
        return bool(self.translation)

    @property
    def has_transliteration(self) -> bool:
        return bool(self.transliteration)

    @property
    def has_context(self) -> bool:
        return bool(self.context)

    @property
    def has_source_reference(self) -> bool:
        return bool(self.source_reference)

    @property
    def word_count(self) -> int:
        return len(self.children)

    @property
    def has_words(self) -> bool:
        return self.word_count > 0

    @property
    def first_word_identifier(self) -> str | None:
        if not self.children:
            return None
        return self.children[0]

    @property
    def last_word_identifier(self) -> str | None:
        if not self.children:
            return None
        return self.children[-1]

    @property
    def is_empty(self) -> bool:
        return self.word_count == 0

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

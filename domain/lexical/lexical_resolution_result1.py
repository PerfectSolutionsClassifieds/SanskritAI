from __future__ import annotations

"""
SanskritAI
==========

Lexical Resolution Result

Specialized ResolutionResult produced by the Lexical Kernel.

Represents the outcome of resolving one lexical concept from a
surface word form.

Relationship
------------

ResolutionResult
        │
        ▼
LexicalResolutionResult
        │
        ├── LexicalEntryCollection
        ├── Preferred LexicalEntry
        ├── Matched Word Form
        ├── Normalized Word Form
        └── Ambiguity Information

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.lexical.lexical_entry import (
    LexicalEntry,
)

from SanskritAI.domain.lexical.lexical_entry_collection import (
    LexicalEntryCollection,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


@dataclass(frozen=True, slots=True)
class LexicalResolutionResult(
    ResolutionResult,
):
    """
    Immutable lexical resolution result.
    """

    lexical_entries: LexicalEntryCollection = (
        LexicalEntryCollection()
    )

    matched_word_form: str = ""

    normalized_word_form: str = ""

    ambiguity_detected: bool = False

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_entries(
        self,
    ) -> bool:
        return self.lexical_entries.has_entries

    @property
    def entry_count(
        self,
    ) -> int:
        return self.lexical_entries.count

    @property
    def preferred_entry(
        self,
    ) -> LexicalEntry | None:
        """
        Returns the preferred lexical entry.

        Currently this is the first entry. Future versions may
        incorporate lexical ranking and semantic scoring.
        """

        return self.lexical_entries.first

    @property
    def is_ambiguous(
        self,
    ) -> bool:
        return self.ambiguity_detected

    @property
    def is_unique(
        self,
    ) -> bool:
        return (
            self.entry_count == 1
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.lexical_entries.is_empty

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Lexical Resolution Result"

    @property
    def display_text(
        self,
    ) -> str:

        return (
            f"{self.entry_count} lexical "
            f"entr{'y' if self.entry_count == 1 else 'ies'}"
        )

    @property
    def display_description(
        self,
    ) -> str:

        if self.normalized_word_form:

            return (
                f"Resolved "
                f"'{self.normalized_word_form}'."
            )

        return "Lexical resolution result."

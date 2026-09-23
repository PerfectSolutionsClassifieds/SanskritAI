from __future__ import annotations

"""
SanskritAI
==========

Lexical Resolution Result

Purpose
-------
Specialized ResolutionResult produced by the Lexical Kernel.

Unlike the previous implementation that returned legacy
LexicalEntry objects, this version returns the canonical
knowledge objects used throughout the Canonical Knowledge
Repository.

Relationship
------------

ResolutionResult
        │
        ▼
LexicalResolutionResult
        │
        ├── CanonicalDictionaryEntry
        ├── CanonicalDictionarySense
        ├── CanonicalContext
        └── CanonicalSource

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LexicalResolutionResult(
    ResolutionResult,
):
    """
    Immutable lexical resolution result.

    Represents the outcome of resolving a surface Sanskrit
    word into canonical lexical knowledge.
    """

    entry: CanonicalDictionaryEntry | None = None

    sense: CanonicalDictionarySense | None = None

    matched_word_form: str = ""

    normalized_word_form: str = ""

    ambiguity_detected: bool = False

    # ---------------------------------------------------------
    # Canonical Objects
    # ---------------------------------------------------------

    @property
    def has_entry(
        self,
    ) -> bool:

        return self.entry is not None

    @property
    def has_sense(
        self,
    ) -> bool:

        return self.sense is not None

    @property
    def context(
        self,
    ) -> CanonicalContext | None:

        if self.sense is None:
            return None

        return self.sense.context

    @property
    def source(
        self,
    ) -> CanonicalSource | None:

        if self.sense is None:
            return None

        return self.sense.source

    # ---------------------------------------------------------
    # Resolution State
    # ---------------------------------------------------------

    @property
    def resolved(
        self,
    ) -> bool:

        return (
            self.succeeded
            and self.has_entry
            and self.has_sense
        )

    @property
    def unresolved(
        self,
    ) -> bool:

        return not self.resolved

    @property
    def is_unique(
        self,
    ) -> bool:

        return (
            self.has_entry
            and not self.ambiguity_detected
        )

    @property
    def is_ambiguous(
        self,
    ) -> bool:

        return self.ambiguity_detected

    @property
    def is_confident(
        self,
    ) -> bool:

        return self.confidence >= 0.80

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def headword(
        self,
    ) -> str | None:

        if self.entry is None:
            return None

        return self.entry.headword

    @property
    def definition(
        self,
    ) -> str | None:

        if self.sense is None:
            return None

        return self.sense.definition

    @property
    def glossary(
        self,
    ) -> str | None:

        if self.sense is None:
            return None

        return self.sense.gloss

    # ---------------------------------------------------------
    # Display
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

        if self.unresolved:
            return "No lexical resolution"

        return (
            f"{self.headword} → "
            f"{self.definition}"
        )

    @property
    def display_description(
        self,
    ) -> str:

        if self.context is None:
            return self.display_text

        return (
            f"{self.display_text} "
            f"({self.context.identifier})"
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text

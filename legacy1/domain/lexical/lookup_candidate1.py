from __future__ import annotations

"""
SanskritAI
==========

Lookup Candidate

Represents one candidate returned by the lexical lookup engine.

A LookupCandidate is a lightweight wrapper around a canonical
dictionary entry together with the matching sense and an
associated ranking score.

Relationship
------------

LexicalLookupEngine
        │
        ▼
LookupCandidate
        │
        ├────────► CanonicalDictionaryEntry
        └────────► CanonicalDictionarySense

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LookupCandidate:
    """
    Immutable lexical lookup candidate.
    """

    entry: CanonicalDictionaryEntry

    sense: CanonicalDictionarySense | None = None

    score: float = 1.0

    matched_word_form: str = ""

    normalized_word_form: str = ""

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        return self.entry.entry_id

    @property
    def headword(
        self,
    ) -> str:
        return self.entry.headword

    @property
    def has_sense(
        self,
    ) -> bool:
        return self.sense is not None

    @property
    def confidence(
        self,
    ) -> float:
        return self.score

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (
            "LookupCandidate("
            f"{self.headword}, "
            f"score={self.score:.3f}"
            ")"
        )

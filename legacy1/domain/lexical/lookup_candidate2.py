
from __future__ import annotations

"""
SanskritAI
==========

Lookup Candidate
----------------

Represents one candidate returned by the lexical lookup engine.

Relationship
------------

LexicalLookupEngine
        │
        ▼
LookupCandidate
        │
        ├────────► CanonicalDictionaryEntry
        │
        └────────► CanonicalDictionarySense

Version
-------
v1.1.0
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

    # =========================================================
    # Convenience
    # =========================================================

    @property
    def identifier(self) -> str:
        """
        Return the canonical source-level entry identity.

        CanonicalDictionaryEntry does not expose ``entry_id``.
        Its source-level identity is represented by
        ``source_record_id``.
        """

        return self.entry.source_record_id

    @property
    def headword(self) -> str:
        return self.entry.headword

    @property
    def has_sense(self) -> bool:
        return self.sense is not None

    @property
    def confidence(self) -> float:
        return self.score

    # =========================================================
    # String representation
    # =========================================================

    def __str__(self) -> str:
        return (
            "LookupCandidate("
            f"{self.headword}, "
            f"score={self.score:.3f}"
            ")"
        )

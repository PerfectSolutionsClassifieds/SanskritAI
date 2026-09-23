from __future__ import annotations

"""
SanskritAI
==========

Canonical Lemma

Purpose
-------
Represents the canonical lexical identity shared by one or more
dictionary entries.

A lemma corresponds to the normalized lexical form used throughout
the Canonical Sanskrit Knowledge Repository.

Architecture
------------

CanonicalLexicon
       │
       ▼
CanonicalLemma
       │
       ▼
CanonicalDictionaryEntry
       │
       ▼
CanonicalDictionarySense

Examples
--------
Lemma
    गम्

Dictionary Entries
    गच्छति
    गतः
    गमनम्
    गन्ता

All belong to the same canonical lemma.

Version
-------
1.1.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLemma:
    """
    Canonical lexical lemma.

    The canonical persisted field is ``lemma``.

    ``lemma_id`` and ``text`` are exposed as compatibility/accessor
    properties for index and repository layers that need a stable
    identifier and textual lookup representation.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    lemma: str

    # ---------------------------------------------------------
    # Optional display / transliteration information
    # ---------------------------------------------------------

    transliteration: str | None = None

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    language: str = "sa"
    script: str = "Devanagari"

    # ---------------------------------------------------------
    # Root Information
    # ---------------------------------------------------------

    dhatu: str | None = None
    part_of_speech: str | None = None
    lexical_category: str | None = None

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Compatibility / Canonical Accessors
    # ---------------------------------------------------------

    @property
    def text(self) -> str:
        """
        Canonical textual representation of the lemma.

        This is intentionally an alias of ``lemma`` so that indexing
        code can use a stable textual lookup API.
        """

        return self.lemma

    @property
    def lemma_id(self) -> str:
        """
        Stable identifier for the lemma.

        Until a separately generated persistent identifier is introduced,
        the canonical lemma text itself serves as the deterministic
        identifier.

        This keeps the current in-memory knowledge layer deterministic
        and avoids introducing an artificial ID-generation mechanism.
        """

        return self.lemma

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> dict:
        return {
            "lemma": self.lemma,
            "lemma_id": self.lemma_id,
            "text": self.text,
            "dhatu": self.dhatu,
            "part_of_speech": self.part_of_speech,
            "category": self.lexical_category,
        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.lemma

    def __str__(self) -> str:
        return (
            "CanonicalLemma("
            f"{self.lemma})"
        )
        

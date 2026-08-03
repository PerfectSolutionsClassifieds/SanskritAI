from __future__ import annotations

"""
SanskritAI
==========

Canonical Dictionary Entry

Purpose
-------
Represents one canonical lexical entry within the
Canonical Sanskrit Knowledge Repository.

Unlike CanonicalLexicalRecord, which is an acquisition
transfer object, CanonicalDictionaryEntry is a stable
domain object used by

    • Reader UI

    • Grammar Engine

    • AI Retrieval

    • Contextual Dictionaries

    • REST APIs

One Dictionary Entry may later contain multiple
Dictionary Senses.

Architecture
------------

CanonicalLexicalRecord

        ↓

CanonicalDictionaryEntry

        ↓

CanonicalDictionarySense

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalDictionaryEntry:
    """
    Canonical lexical entry.

    One entry represents one Sanskrit lexical headword.

    Context-specific meanings are intentionally NOT stored
    here; they belong to CanonicalDictionarySense.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    headword: str

    transliteration: str | None = None

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    language: str = "sa"

    script: str = "Devanagari"

    # ---------------------------------------------------------
    # Lexical Metadata
    # ---------------------------------------------------------

    lemma: str | None = None

    normalized_headword: str | None = None

    entry_type: str | None = None

    # ---------------------------------------------------------
    # Source Information
    # ---------------------------------------------------------

    source_name: str = ""

    source_version: str = ""

    source_record_id: str = ""

    citation: str | None = None

    # ---------------------------------------------------------
    # Repository Metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "headword": self.headword,

            "lemma": self.lemma,

            "source": self.source_name,

            "entry_type": self.entry_type,

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return self.headword

    @property
    def has_transliteration(
        self,
    ) -> bool:

        return self.transliteration is not None

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalDictionaryEntry("
            f"{self.headword})"
        )

from __future__ import annotations

"""
SanskritAI
==========

Canonical Lemma

Purpose
-------
Represents the canonical lexical identity shared by one or
more dictionary entries.

A lemma corresponds to the normalized lexical form used
throughout the Canonical Sanskrit Knowledge Repository.

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
class CanonicalLemma:
    """
    Canonical lexical lemma.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    lemma: str

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
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "lemma": self.lemma,

            "dhatu": self.dhatu,

            "part_of_speech": self.part_of_speech,

            "category": self.lexical_category,

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return self.lemma

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalLemma("
            f"{self.lemma})"
        )

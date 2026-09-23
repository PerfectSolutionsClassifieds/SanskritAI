from __future__ import annotations

"""
SanskritAI
==========

Canonical Lexical Record

Purpose
-------
Defines the canonical intermediate lexical representation
used throughout the SanskritAI acquisition pipeline.

Every lexical resource

    • Monier–Williams
    • Apte
    • Amarakośa
    • Śabdakalpadruma
    • Vācaspatyam
    • Dhātupāṭha
    • Gaṇapāṭha
    • Uṇādi

is transformed into this common representation before
entering the CanonicalLexicalRepository.

Pipeline
--------

RawLexicalEntry

        ↓

CanonicalLexicalRecord

        ↓

CanonicalLexicalRepository

        ↓

Lexeme

        ↓

DictionaryEntry

        ↓

DictionarySense

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLexicalRecord:
    """
    Canonical lexical record shared by every lexical
    acquisition pipeline.
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
    # Lexical Information
    # ---------------------------------------------------------

    definition: str = ""

    entry_type: str | None = None

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    source_name: str = ""

    source_version: str = ""

    source_record_id: str = ""

    citation: str | None = None

    # ---------------------------------------------------------
    # Extension Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(
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

            "source": self.source_name,

            "version": self.source_version,

            "entry_type": self.entry_type,

        }

    def __str__(
        self,
    ) -> str:

        return (
            f"CanonicalLexicalRecord("
            f"{self.headword})"
        )

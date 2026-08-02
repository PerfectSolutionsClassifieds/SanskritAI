from __future__ import annotations

"""
SanskritAI
==========

Raw Lexical Entry

Purpose
-------
Represents ONE lexical record exactly as extracted from an
external lexical resource, before any canonical normalization.

This is the canonical intermediate representation shared by
all lexical parsers.

Examples
--------

Monier-Williams
Apte
Amarakośa
Śabdakalpadruma
Vācaspatyam
Dhātupāṭha
Gaṇapāṭha
Uṇādi

All parsers should return RawLexicalEntry objects.

Architecture
------------

External Source

        ↓

Parser

        ↓

RawLexicalEntry

        ↓

Transformer

        ↓

Canonical Lexical Entry

Design Principles
-----------------

• Immutable
• Lossless
• Preserve source wording
• Preserve provenance
• No interpretation
• No normalization
• No grammatical inference

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
class RawLexicalEntry:
    """
    Immutable lexical record extracted directly from
    an external resource.
    """

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    source_name: str

    source_version: str

    source_record_id: str

    source_url: str | None = None

    citation: str | None = None

    license: str | None = None

    # ---------------------------------------------------------
    # Raw lexical data
    # ---------------------------------------------------------

    headword: str = ""

    raw_text: str = ""

    language: str = "sa"

    script: str = "Devanagari"

    # ---------------------------------------------------------
    # Optional parser hints
    # ---------------------------------------------------------

    transliteration: str | None = None

    entry_type: str | None = None

    section: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def has_headword(
        self,
    ) -> bool:
        """
        Returns True if a headword exists.
        """
        return bool(
            self.headword.strip(),
        )

    @property
    def has_raw_text(
        self,
    ) -> bool:
        """
        Returns True if raw entry text exists.
        """
        return bool(
            self.raw_text.strip(),
        )

    def summary(
        self,
    ) -> dict:
        """
        Lightweight diagnostic summary.
        """
        return {
            "source": self.source_name,
            "record_id": self.source_record_id,
            "headword": self.headword,
            "script": self.script,
            "language": self.language,
            "entry_type": self.entry_type,
        }

    def __str__(
        self,
    ) -> str:
        return (
            "RawLexicalEntry("
            f"{self.source_name}: "
            f"{self.headword})"
        )

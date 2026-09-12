from __future__ import annotations

"""
SanskritAI
==========

Synset Record

Immutable parser record representing a single Amarakośa
synset.

A SynsetRecord is the canonical parser output exchanged
between parsers, validators and record builders.

Pipeline
--------

Parser
    ↓
SynsetRecord
    ↓
SynsetValidator
    ↓
SynsetRecordBuilder
    ↓
Synset

Version
-------
v0.4.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.records.knowledge_record import (
    KnowledgeRecord,
)
from SanskritAI.amarakosha.enums.Amarakanda import (
    Amarakanda,
)


@dataclass(slots=True, frozen=True)
class SynsetRecord(KnowledgeRecord[str]):
    """
    Immutable parser representation of an Amarakośa Synset.
    """

    # ---------------------------------------------------------
    # Amarakośa location
    # ---------------------------------------------------------

    kanda: Amarakanda

    varga: str

    verse: int

    sequence: int = 1

    # ---------------------------------------------------------
    # Canonical text
    # ---------------------------------------------------------

    devanagari: str = ""

    iast: str = ""

    transliteration: str = ""

    # ---------------------------------------------------------
    # Semantic information
    # ---------------------------------------------------------

    gloss: str = ""

    # ---------------------------------------------------------
    # Lexical references
    # ---------------------------------------------------------

    lexeme_ids: tuple[str, ...] = field(
        default_factory=tuple
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    tags: tuple[str, ...] = field(
        default_factory=tuple
    )

    notes: str = ""

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_text(self) -> str:
        """
        Preferred display representation.
        """
        return (
            self.devanagari
            or self.iast
            or self.transliteration
        )

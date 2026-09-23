from __future__ import annotations

"""
SanskritAI
==========

Varga Record

Immutable parser record representing a single Amarakośa
Varga.

A VargaRecord is the canonical parser output exchanged
between parsers, validators and record builders.

Pipeline
--------

Parser
    ↓
VargaRecord
    ↓
VargaValidator
    ↓
VargaRecordBuilder
    ↓
Varga

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
class VargaRecord(KnowledgeRecord[str]):
    """
    Immutable parser representation of an Amarakośa Varga.
    """

    # ---------------------------------------------------------
    # Amarakośa location
    # ---------------------------------------------------------

    kanda: Amarakanda

    varga_number: int

    # ---------------------------------------------------------
    # Canonical title
    # ---------------------------------------------------------

    name: str

    title: str

    # ---------------------------------------------------------
    # Canonical text
    # ---------------------------------------------------------

    devanagari: str = ""

    iast: str = ""

    transliteration: str = ""

    # ---------------------------------------------------------
    # Description
    # ---------------------------------------------------------

    description: str = ""

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
            or self.title
            or self.name
        )

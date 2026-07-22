from __future__ import annotations

"""
SanskritAI
==========

Data Record

The immutable root record for the SanskritAI platform.

DataRecord represents the canonical transfer object exchanged
between architectural layers such as:

    Parser
        ↓
    Builder
        ↓
    Repository
        ↓
    Registry
        ↓
    Importer / Exporter

All domain-specific records derive from this class.

Examples
--------
CorpusRecord
LexicalRecord
KnowledgeRecord
TrainingRecord (future)
EmbeddingRecord (future)

Version
-------
v0.4.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic

from SanskritAI.core.typing import TIdentifier


@dataclass(slots=True, frozen=True)
class DataRecord(Generic[TIdentifier]):
    """
    Immutable base class for all SanskritAI records.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    identifier: TIdentifier

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    source: str = ""

    source_identifier: str = ""

    source_version: str = ""

    # ---------------------------------------------------------
    # Audit
    # ---------------------------------------------------------

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    active: bool = True

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_source(self) -> bool:
        """
        Returns True if the record originated from an external
        source.
        """
        return bool(self.source)

    @property
    def is_active(self) -> bool:
        """
        Indicates whether this record is active.
        """
        return self.active

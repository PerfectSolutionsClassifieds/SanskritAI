from __future__ import annotations

"""
SanskritAI
==========

Provenance

Captures how a resource entered SanskritAI.

Version
-------
v0.1.0
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC

from SanskritAI.common.metadata.confidence_score import (
    ConfidenceScore,
)
from SanskritAI.common.metadata.source_reference import (
    SourceReference,
)


@dataclass(slots=True)
class Provenance:
    """
    Provenance metadata shared across SanskritAI.
    """

    source: SourceReference

    confidence: ConfidenceScore = field(
        default_factory=lambda: ConfidenceScore(1.0)
    )

    acquired_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    notes: list[str] = field(
        default_factory=list
    )

    def add_note(
        self,
        note: str,
    ) -> None:

        self.notes.append(note)

    def to_dict(self) -> dict:

        return {

            "source":
                self.source.to_dict(),

            "confidence":
                self.confidence.to_dict(),

            "acquired_at":
                self.acquired_at.isoformat(),

            "notes":
                list(self.notes),

        }

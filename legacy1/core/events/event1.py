from __future__ import annotations

"""
SanskritAI
==========

Core Event

Defines the immutable base class for all domain events within
the SanskritAI Architectural Kernel.

An Event represents something that has already occurred.

Examples
--------

CorpusCreatedEvent
DocumentAddedEvent
VerseParsedEvent
LexemeImportedEvent
MorphologyAnalyzedEvent

Version
-------
v0.3.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Event:
    """
    Immutable base class for all domain events.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    event_id: UUID = field(
        default_factory=uuid4,
    )

    # ---------------------------------------------------------
    # Time
    # ---------------------------------------------------------

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc,
        )
    )

    # ---------------------------------------------------------
    # Optional payload
    # ---------------------------------------------------------

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Event class name.
        """

        return self.__class__.__name__

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the event.
        """

        return {
            "event_id": str(self.event_id),
            "name": self.name,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
        }

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.name}"
            f"(id={self.event_id}, "
            f"time={self.timestamp.isoformat()})"
        )

from __future__ import annotations

"""
SanskritAI
==========

Core Event

Defines the immutable runtime occurrence of a domain event.

An Event represents something that has already occurred.
Its semantic identity is described by EventMetadata,
while Event itself captures the runtime occurrence
(timestamp and payload).

Architecture
------------

EventMetadata
      │
      ▼
Event
      │
      ▼
Infrastructure
(EventEnvelope, EventBus, etc.)

Version
-------
v0.7.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from SanskritAI.core.events.event_metadata import EventMetadata
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Event(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime occurrence of a domain event.
    """

    metadata: EventMetadata

    event_instance_id: UUID = field(
        default_factory=uuid4,
    )

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc,
        ),
    )

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def identifier(self) -> str:
        """
        Returns the runtime occurrence identifier.
        """
        return str(self.occurrence_id)

    @property
    def event_identifier(self) -> str:
        """
        Returns the semantic event identifier.
        """
        return self.metadata.identifier

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

    @property
    def display_text(self) -> str:
        return self.metadata.display_text

    @property
    def display_description(self) -> str:
        return self.metadata.display_description

    @property
    def name(self) -> str:
        """
        Compatibility alias.
        """
        return self.display_name

    @property
    def event_type(self):
        return self.metadata.event_type

    @property
    def priority(self):
        return self.metadata.priority

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the event occurrence.
        """
        return {
            "event_instance_id": self.identifier,
            "event_id": self.event_identifier,
            "event_type": self.event_type.identifier,
            "priority": self.priority.identifier,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
        }

    def __repr__(self) -> str:
        return (
            f"{self.display_name}"
            f"(occurrence={self.identifier}, "
            f"event={self.event_identifier})"
        )

    def __str__(self) -> str:
        return self.display_text

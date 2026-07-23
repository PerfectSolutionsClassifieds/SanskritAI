from __future__ import annotations

"""
SanskritAI
==========

Event Envelope

Defines the immutable transport envelope for an Event.

An EventEnvelope wraps a domain Event together with optional
transport metadata used by the Infrastructure kernel.

The Events kernel remains completely unaware of envelopes.

Architecture
------------

Event
    │
    ▼
EventEnvelope
    │
    ▼
EventBus

Version
-------
v0.7.0
"""

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from SanskritAI.core.events.event import Event
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventEnvelope(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable transport envelope for a domain event.
    """

    event: Event

    envelope_id: UUID = field(
        default_factory=uuid4,
    )

    correlation_id: UUID | None = None

    causation_id: UUID | None = None

    headers: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def identifier(self) -> str:
        """
        Returns the envelope identifier.
        """
        return str(self.envelope_id)

    @property
    def display_name(self) -> str:
        return "Event Envelope"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.event.display_name})"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable transport wrapper for a domain event."
        )

    @property
    def event_identifier(self) -> str:
        """
        Returns the wrapped semantic event identifier.
        """
        return self.event.event_identifier

    @property
    def event_instance_id(self) -> str:
        """
        Returns the wrapped runtime event instance identifier.
        """
        return self.event.identifier

    @property
    def event_type(self):
        """
        Returns the wrapped event type.
        """
        return self.event.event_type

    @property
    def priority(self):
        """
        Returns the wrapped event priority.
        """
        return self.event.priority

    def with_header(
        self,
        key: str,
        value: Any,
    ) -> "EventEnvelope":
        """
        Returns a new envelope with an additional header.
        """
        updated_headers = dict(self.headers)
        updated_headers[key] = value

        return EventEnvelope(
            event=self.event,
            envelope_id=self.envelope_id,
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            headers=updated_headers,
        )

    def __str__(self) -> str:
        return self.display_text

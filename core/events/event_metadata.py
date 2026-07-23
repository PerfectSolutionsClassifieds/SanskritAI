from __future__ import annotations

"""
SanskritAI
==========

Event Metadata

Defines the immutable semantic metadata describing an event.

Unlike Event, EventMetadata contains only descriptive
information and no runtime state.

Architecture
------------

EventId
    │
    ├── EventType
    ├── EventPriority
    │
    ▼
EventMetadata
    │
    ▼
Event

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.events.event_id import EventId
from SanskritAI.core.events.event_priority import EventPriority
from SanskritAI.core.events.event_type import EventType
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing an event.
    """

    event_id: EventId

    event_type: EventType = EventType.DOMAIN

    priority: EventPriority = EventPriority.NORMAL

    description: str = ""

    @property
    def identifier(self) -> str:
        return self.event_id.identifier

    @property
    def display_name(self) -> str:
        return self.event_id.display_name

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name} "
            f"[{self.event_type.display_name}]"
        )

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def is_critical(self) -> bool:
        """
        Indicates whether the event has critical priority.
        """
        return self.priority is EventPriority.CRITICAL

    def __str__(self) -> str:
        return self.display_text

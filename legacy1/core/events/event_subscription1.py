from __future__ import annotations

"""
SanskritAI
==========

Event Subscription

Defines the immutable association between an EventHandler
and an EventType.

Subscriptions represent registration semantics rather than
handler implementation. Runtime dispatching belongs to the
Infrastructure kernel.

Architecture
------------

EventHandler
      │
      ▼
EventSubscription
      │
      ▼
EventRegistry

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.events.event import Event
from SanskritAI.core.events.event_handler import EventHandler
from SanskritAI.core.events.event_priority import EventPriority
from SanskritAI.core.events.event_type import EventType
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventSubscription(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable event subscription.
    """

    handler: EventHandler

    event_type: EventType

    priority: EventPriority = EventPriority.NORMAL

    enabled: bool = True

    @property
    def identifier(self) -> str:
        """
        Canonical subscription identifier.
        """
        return (
            f"{self.handler.identifier}:"
            f"{self.event_type.identifier}"
        )

    @property
    def display_name(self) -> str:
        return self.identifier

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            f"Subscription for "
            f"{self.event_type.display_name} events."
        )

    def supports(
        self,
        event: Event,
    ) -> bool:
        """
        Determines whether this subscription accepts the event.
        """
        return (
            self.enabled
            and event.event_type is self.event_type
        )

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Event Subscriber

Defines the canonical synchronous event subscriber.

An EventSubscriber owns subscription management while
delegating registration to the underlying EventBus.

Architecture
------------

EventSubscriber
        │
        ▼
EventChannel
        │
        ▼
EventBus

Version
-------
v0.7.0
"""

from dataclasses import dataclass
from collections.abc import Callable

from SanskritAI.core.events.event_type import EventType
from SanskritAI.core.infrastructure.event_channel import EventChannel
from SanskritAI.core.infrastructure.event_envelope import EventEnvelope
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


EventHandler = Callable[[EventEnvelope], None]


@dataclass(frozen=True, slots=True)
class EventSubscriber(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable event subscriber.
    """

    channel: EventChannel

    @property
    def identifier(self) -> str:
        return "event_subscriber"

    @property
    def display_name(self) -> str:
        return "Event Subscriber"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Registers and removes event handlers."
        )

    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Registers an event handler.
        """
        self.channel.bus.subscribe(
            event_type,
            handler,
        )

    def unsubscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Removes an event handler.
        """
        self.channel.bus.unsubscribe(
            event_type,
            handler,
        )

    def __str__(self) -> str:
        return self.display_text

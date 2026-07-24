from __future__ import annotations

"""
SanskritAI
==========

Event Channel

Defines a logical channel for synchronous event dispatch.

An EventChannel groups events under a semantic identifier
while delegating dispatch to an EventBus.

The channel owns no queues, persistence, routing,
or asynchronous behavior.

Architecture
------------

EventEnvelope
      │
      ▼
EventBus
      │
      ▼
EventChannel
      │
      ▼
EventPublisher

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.event_bus import EventBus
from SanskritAI.core.infrastructure.event_envelope import EventEnvelope
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventChannel(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable logical event channel.
    """

    identifier: str

    bus: EventBus

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.identifier.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    def publish(
        self,
        envelope: EventEnvelope,
    ) -> int:
        """
        Publishes an envelope through the underlying bus.

        Returns
        -------
        int
            Number of invoked handlers.
        """
        return self.bus.publish(envelope)

    def __str__(self) -> str:
        return self.display_text

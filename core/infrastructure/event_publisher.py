from __future__ import annotations

"""
SanskritAI
==========

Event Publisher

Defines the canonical synchronous event publisher.

An EventPublisher publishes immutable EventEnvelope instances
through an EventChannel.

The publisher owns no routing, middleware, retries,
or asynchronous behavior.

Architecture
------------

EventEnvelope
      │
      ▼
EventPublisher
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

from SanskritAI.core.infrastructure.event_channel import EventChannel
from SanskritAI.core.infrastructure.event_envelope import EventEnvelope
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventPublisher(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable event publisher.
    """

    channel: EventChannel

    @property
    def identifier(self) -> str:
        return "event_publisher"

    @property
    def display_name(self) -> str:
        return "Event Publisher"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Publishes immutable event envelopes."
        )

    def publish(
        self,
        envelope: EventEnvelope,
    ) -> int:
        """
        Publishes an envelope through the channel.

        Returns
        -------
        int
            Number of invoked handlers.
        """
        return self.channel.publish(envelope)

    def __call__(
        self,
        envelope: EventEnvelope,
    ) -> int:
        return self.publish(envelope)

    def __str__(self) -> str:
        return self.display_text

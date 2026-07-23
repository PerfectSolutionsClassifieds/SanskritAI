from __future__ import annotations

"""
SanskritAI
==========

Event Registry

Defines the immutable registry of event subscriptions.

The registry is declarative and does not perform dispatching.
Runtime event routing belongs to EventDispatcher and the
Infrastructure kernel.

Architecture
------------

EventSubscription
        │
        ▼
EventRegistry
        │
        ▼
EventDispatcher

Version
-------
v0.7.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.events.event import Event
from SanskritAI.core.events.event_subscription import EventSubscription
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventRegistry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable registry of event subscriptions.
    """

    subscriptions: frozenset[EventSubscription] = field(
        default_factory=frozenset,
    )

    @property
    def identifier(self) -> str:
        return "event_registry"

    @property
    def display_name(self) -> str:
        return "Event Registry"

    @property
    def display_text(self) -> str:
        return (
            f"Event Registry "
            f"({len(self.subscriptions)} subscriptions)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable registry of event subscriptions."
        )

    def subscriptions_for(
        self,
        event: Event,
    ) -> tuple[EventSubscription, ...]:
        """
        Returns the subscriptions that support the supplied event,
        ordered by priority.
        """
        matching = (
            subscription
            for subscription in self.subscriptions
            if subscription.supports(event)
        )

        return tuple(
            sorted(
                matching,
                key=lambda subscription: subscription.priority,
            )
        )

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether a subscription exists.
        """
        normalized = identifier.strip()

        return any(
            subscription.identifier == normalized
            for subscription in self.subscriptions
        )

    def __len__(self) -> int:
        return len(self.subscriptions)

    def __iter__(self):
        return iter(self.subscriptions)

    def __str__(self) -> str:
        return self.display_text

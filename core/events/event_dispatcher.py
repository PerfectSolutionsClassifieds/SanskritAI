from __future__ import annotations

"""
SanskritAI
==========

Event Dispatcher

Defines the canonical synchronous dispatcher for domain events.

The dispatcher is intentionally lightweight. It performs only
deterministic in-process dispatch using the EventRegistry.

Advanced runtime capabilities such as asynchronous messaging,
event buses, middleware pipelines, retries, correlation IDs,
and transport belong to the Infrastructure kernel.

Architecture
------------

Event
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

from dataclasses import dataclass

from SanskritAI.core.events.event import Event
from SanskritAI.core.events.event_registry import EventRegistry
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventDispatcher(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical synchronous event dispatcher.
    """

    registry: EventRegistry

    @property
    def identifier(self) -> str:
        return "event_dispatcher"

    @property
    def display_name(self) -> str:
        return "Event Dispatcher"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Synchronously dispatches events using the "
            "registered subscriptions."
        )

    def dispatch(
        self,
        event: Event,
    ) -> int:
        """
        Dispatches an event.

        Returns
        -------
        int
            Number of invoked subscriptions.
        """
        subscriptions = self.registry.subscriptions_for(
            event,
        )

        for subscription in subscriptions:
            subscription.invoke(event)

        return len(subscriptions)

    def __call__(
        self,
        event: Event,
    ) -> int:
        """
        Callable shortcut for dispatch().
        """
        return self.dispatch(event)

    def __str__(self) -> str:
        return self.display_text

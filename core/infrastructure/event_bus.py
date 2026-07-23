from __future__ import annotations

"""
SanskritAI
==========

Event Bus

Lightweight synchronous publish/subscribe event bus.

The EventBus operates on immutable EventEnvelope instances
and dispatches them according to their semantic EventType.

The bus is intentionally lightweight.

It does NOT implement:

- asynchronous execution
- retries
- persistence
- middleware
- queues
- routing

Those capabilities belong to higher infrastructure layers.

Architecture
------------

EventEnvelope
      │
      ▼
EventBus
      │
      ▼
EventPublisher
      │
      ▼
EventSubscriber

Version
-------
v0.7.0
"""

from collections import defaultdict
from collections.abc import Callable

from SanskritAI.core.events.event_type import EventType
from SanskritAI.core.infrastructure.event_envelope import EventEnvelope


EventHandler = Callable[[EventEnvelope], None]


class EventBus:
    """
    Lightweight synchronous event bus.
    """

    def __init__(self) -> None:
        self._handlers: dict[
            EventType,
            list[EventHandler],
        ] = defaultdict(list)

    # ---------------------------------------------------------
    # Subscription
    # ---------------------------------------------------------

    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Registers a handler for an event type.

        Duplicate registrations are ignored.
        """

        handlers = self._handlers[event_type]

        if handler not in handlers:
            handlers.append(handler)

    # ---------------------------------------------------------

    def unsubscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Removes a handler.
        """

        handlers = self._handlers.get(event_type)

        if handlers and handler in handlers:

            handlers.remove(handler)

            if not handlers:
                del self._handlers[event_type]

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    def publish(
        self,
        envelope: EventEnvelope,
    ) -> int:
        """
        Publishes an event envelope.

        Returns
        -------
        int
            Number of invoked handlers.
        """

        handlers = tuple(
            self._handlers.get(
                envelope.event_type,
                (),
            )
        )

        for handler in handlers:
            handler(envelope)

        return len(handlers)

    # ---------------------------------------------------------
    # Introspection
    # ---------------------------------------------------------

    def subscribed_event_types(
        self,
    ) -> tuple[EventType, ...]:
        """
        Returns all subscribed event types.
        """

        return tuple(self._handlers.keys())

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Removes every subscription.
        """

        self._handlers.clear()

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Number of subscribed event types.
        """

        return len(self._handlers)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        return (
            f"EventBus("
            f"event_types={len(self)})"
        )

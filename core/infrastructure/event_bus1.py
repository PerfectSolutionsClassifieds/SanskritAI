
from __future__ import annotations

"""
SanskritAI
==========

Event Bus

Lightweight synchronous publish/subscribe event bus for the
SanskritAI Architectural Kernel.

The EventBus is intentionally domain-agnostic. It dispatches
immutable Event objects to subscribed handlers.

Version
-------
v0.3.0
"""

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from SanskritAI.core.events.event import Event

EventHandler = Callable[[Event], None]


class EventBus:
    """
    Lightweight synchronous event bus.
    """

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandler]] = (
            defaultdict(list)
        )

    # ---------------------------------------------------------
    # Subscription
    # ---------------------------------------------------------

    def subscribe(
        self,
        event_type: type[Event],
        handler: EventHandler,
    ) -> None:
        """
        Subscribe a handler to an event type.

        Duplicate subscriptions are ignored.
        """

        handlers = self._handlers[event_type]

        if handler not in handlers:
            handlers.append(handler)

    # ---------------------------------------------------------

    def unsubscribe(
        self,
        event_type: type[Event],
        handler: EventHandler,
    ) -> None:
        """
        Remove a handler from an event type.
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
        event: Event,
    ) -> None:
        """
        Publish an event.

        Handlers subscribed to any superclass of the event
        are also invoked.
        """

        for registered_type, handlers in self._handlers.items():

            if isinstance(event, registered_type):

                for handler in tuple(handlers):
                    handler(event)

    # ---------------------------------------------------------
    # Introspection
    # ---------------------------------------------------------

    def subscribed_event_types(
        self,
    ) -> tuple[type[Event], ...]:
        """
        Return all subscribed event types.
        """

        return tuple(self._handlers.keys())

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove all subscriptions.
        """

        self._handlers.clear()

    # ---------------------------------------------------------

    def __len__(self) -> int:
        """
        Number of registered event types.
        """

        return len(self._handlers)

    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"EventBus("
            f"event_types={len(self)})"
        )

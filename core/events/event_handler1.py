from __future__ import annotations

"""
SanskritAI
==========

Event Handler

Defines the immutable description of an event handler.

An EventHandler describes a callable capable of handling
a particular category of events. It does not perform
dispatching itself; runtime invocation belongs to the
EventDispatcher and Infrastructure kernel.

Architecture
------------

Event
    │
    ▼
EventHandler
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
from typing import Callable

from SanskritAI.core.events.event import Event
from SanskritAI.core.events.event_type import EventType
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class EventHandler(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable description of an event handler.
    """

    identifier: str

    event_type: EventType

    handler: Callable[[Event], None]

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

    def supports(
        self,
        event: Event,
    ) -> bool:
        """
        Determines whether this handler supports the event.
        """
        return event.event_type is self.event_type

    def __call__(
        self,
        event: Event,
    ) -> None:
        """
        Invokes the handler.
        """
        self.handler(event)

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Event Handler

Defines the immutable description of an event handler.

An EventHandler describes only *how* an event is handled.
Registration semantics belong to EventSubscription.

Architecture
------------

Event
    │
    ▼
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
from typing import Callable

from SanskritAI.core.events.event import Event
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
    Immutable event handler descriptor.
    """

    identifier: str

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

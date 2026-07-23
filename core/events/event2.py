from __future__ import annotations

"""
SanskritAI
==========

Core Event

Defines the immutable base class for all domain events.

An Event represents something that has already occurred.

Version
-------
v0.7.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Event(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable base class for all domain events.
    """

    event_id: UUID = field(
        default_factory=uuid4,
    )

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc,
        ),
    )

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def identifier(self) -> str:
        """
        Canonical event identifier.
        """
        return str(self.event_id)

    @property
    def display_name(self) -> str:
        """
        Human-readable event name.
        """
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        """
        Canonical display representation.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Event description.
        """
        return (
            f"{self.display_name} "
            f"occurred at "
            f"{self.timestamp.isoformat()}."
        )

    @property
    def name(self) -> str:
        """
        Alias for compatibility.
        """
        return self.display_name

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the event.
        """
        return {
            "event_id": self.identifier,
            "name": self.name,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
        }

    def __repr__(self) -> str:
        return (
            f"{self.name}"
            f"(id={self.identifier}, "
            f"time={self.timestamp.isoformat()})"
        )

    def __str__(self) -> str:
        return self.display_text

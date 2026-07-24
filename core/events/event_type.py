from __future__ import annotations

"""
SanskritAI
==========

Event Type

Defines the canonical semantic categories of domain events.

An EventType classifies the nature of an event independently
of its payload or runtime transport.

Architecture
------------

EventType
      │
      ▼
EventMetadata
      │
      ▼
Event

Version
-------
v0.7.0
"""

from enum import Enum
from enum import unique


@unique
class EventType(Enum):
    """
    Canonical semantic categories of events.
    """

    DOMAIN = "domain"

    SYSTEM = "system"

    APPLICATION = "application"

    RESOURCE = "resource"

    PLUGIN = "plugin"

    CONFIGURATION = "configuration"

    SEARCH = "search"

    DIAGNOSTIC = "diagnostic"

    LIFECYCLE = "lifecycle"

    CUSTOM = "custom"

    @property
    def identifier(self) -> str:
        """
        Returns the canonical identifier.
        """
        return self.value

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable event type.
        """
        return self.value.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Returns a brief description.
        """
        return (
            f"{self.display_name} event type."
        )

    def __str__(self) -> str:
        return self.display_name

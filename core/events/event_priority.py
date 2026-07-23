from __future__ import annotations

"""
SanskritAI
==========

Event Priority

Defines the canonical priority levels for domain events.

Priorities provide a semantic ordering for event processing.
The Events kernel only defines the ordering; actual scheduling
and dispatch policies belong to the Infrastructure kernel.

Architecture
------------

EventPriority
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

from enum import IntEnum
from enum import unique


@unique
class EventPriority(IntEnum):
    """
    Canonical event priorities.

    Lower numeric values indicate higher priority.
    """

    CRITICAL = 0

    HIGH = 10

    NORMAL = 20

    LOW = 30

    BACKGROUND = 40

    @property
    def identifier(self) -> str:
        """
        Returns the canonical identifier.
        """
        return self.name.lower()

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable priority.
        """
        return self.name.title()

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
        return f"{self.display_name} priority."

    def __str__(self) -> str:
        return self.display_name

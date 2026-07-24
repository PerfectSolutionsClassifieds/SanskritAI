from __future__ import annotations

"""
Resource State.

Version
-------
v0.7.0
"""

from enum import Enum
from enum import unique


@unique
class ResourceState(Enum):

    REGISTERED = "registered"

    AVAILABLE = "available"

    LOADED = "loaded"

    UNAVAILABLE = "unavailable"

    FAILED = "failed"

    ARCHIVED = "archived"

    @property
    def identifier(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        return self.value.title()

    def __str__(self) -> str:
        return self.display_name

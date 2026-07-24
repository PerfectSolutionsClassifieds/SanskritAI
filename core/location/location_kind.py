from __future__ import annotations

"""
SanskritAI
==========

Location Kind

Defines the canonical kinds of locations.

Version
-------
v0.7.0
"""

from enum import Enum
from enum import unique


@unique
class LocationKind(Enum):
    """
    Canonical location kinds.
    """

    FILESYSTEM = "filesystem"

    URI = "uri"

    PACKAGE = "package"

    DATABASE = "database"

    MEMORY = "memory"

    ARCHIVE = "archive"

    CLOUD = "cloud"

    @property
    def identifier(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        return self.value.replace("_", " ").title()

    def __str__(self) -> str:
        return self.display_name

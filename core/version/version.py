from __future__ import annotations

"""
SanskritAI
==========

Version

Defines the canonical immutable representation of a software,
resource, or data version.

Unlike SemanticVersion, Version intentionally makes no assumptions
about formatting. It simply represents an immutable version string.

Examples
--------

1

2026.07

v2

0.7.0

2026.07-beta

Architecture
------------

ValueObject
      │
      ▼
Version
      │
      ▼
SemanticVersion

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Version(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable version identifier.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "Version cannot be empty."
            )

        object.__setattr__(self, "value", normalized)

    @property
    def identifier(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        return self.value

    @property
    def display_text(self) -> str:
        return self.value

    @property
    def display_description(self) -> str:
        return f"Version {self.value}"

    def matches(
        self,
        value: str,
    ) -> bool:
        return self.value == value.strip()

    def __str__(self) -> str:
        return self.value

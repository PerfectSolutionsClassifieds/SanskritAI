from __future__ import annotations

"""
SanskritAI
==========

Configuration Source

Defines the canonical immutable origin of configuration data.

A ConfigurationSource describes where configuration entries
originate. It is intentionally represented as an immutable value
object rather than an enumeration, allowing new sources to be
introduced without modifying the core architecture.

Typical examples include:

- defaults
- environment
- yaml
- json
- toml
- ini
- cli
- django
- postgres
- redis
- remote

Architecture
------------

ValueObject
      │
      ▼
ConfigurationSource
      │
      ▼
ConfigurationProfile

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationSource(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable configuration source.
    """

    name: str

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Configuration source cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the canonical source identifier.
        """
        return self.name

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable source name.
        """
        return self.name.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Returns the optional source description.
        """
        return self.description

    def matches(
        self,
        name: str,
    ) -> bool:
        """
        Determines whether the supplied source name matches this
        configuration source.
        """
        return self.name == name.strip().lower()

    def __str__(self) -> str:
        return self.display_name

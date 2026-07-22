from __future__ import annotations

"""
SanskritAI
==========

Configuration Profile

Defines the immutable effective configuration of a runtime
component.

A ConfigurationProfile associates a named component with its
resolved configuration. The profile itself is independent of
where the configuration originated; configuration provenance is
represented separately by ConfigurationSource.

Typical examples include:

- Paninian Parser
- Amarakośa Dictionary
- Corpus Loader
- AI Embedding Backend
- Django Web Application

Architecture
------------

ValueObject
      │
      ▼
ConfigurationProfile
      │
      ├── name
      └── Configuration

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.configuration.configuration import Configuration
from SanskritAI.core.configuration.configuration_entry import ConfigurationEntry
from SanskritAI.core.configuration.configuration_key import ConfigurationKey
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationProfile(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable configuration profile of a component.
    """

    name: str

    configuration: Configuration

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip()

        if not normalized:
            raise ValueError(
                "Configuration profile name cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the canonical profile identifier.
        """
        return self.name

    @property
    def count(self) -> int:
        """
        Returns the number of configuration entries.
        """
        return len(self.configuration)

    def contains(
        self,
        key: ConfigurationKey,
    ) -> bool:
        """
        Determines whether the supplied key exists.
        """
        return self.configuration.contains(key)

    def lookup(
        self,
        key: ConfigurationKey,
    ) -> ConfigurationEntry | None:
        """
        Looks up a configuration entry.
        """
        return self.configuration.lookup(key)

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return f"{self.name} ({self.count} entries)"

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_text

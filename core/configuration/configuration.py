from __future__ import annotations

"""
SanskritAI
==========

Configuration

Defines the canonical immutable collection of configuration
entries.

Configuration is built around immutable ConfigurationEntry
objects rather than raw dictionaries. It serves as the primary
runtime configuration model throughout the SanskritAI
architecture.

Architecture
------------

ValueObject
      │
      ▼
Configuration
      │
      └── frozenset[ConfigurationEntry]

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from collections.abc import Iterator

from SanskritAI.core.configuration.configuration_entry import (
    ConfigurationEntry,
)
from SanskritAI.core.configuration.configuration_key import (
    ConfigurationKey,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Configuration(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of configuration entries.
    """

    entries: frozenset[ConfigurationEntry] = field(
        default_factory=frozenset
    )

    @property
    def count(self) -> int:
        """
        Returns the number of configuration entries.
        """
        return len(self.entries)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the configuration contains no entries.
        """
        return self.count == 0

    def contains(
        self,
        key: ConfigurationKey,
    ) -> bool:
        """
        Determines whether the supplied key exists.
        """
        return self.lookup(key) is not None

    def lookup(
        self,
        key: ConfigurationKey,
    ) -> ConfigurationEntry | None:
        """
        Looks up a configuration entry by key.
        """
        for entry in self.entries:
            if entry.key == key:
                return entry

        return None

    def add(
        self,
        entry: ConfigurationEntry,
    ) -> "Configuration":
        """
        Returns a new configuration containing the supplied
        entry.

        Any existing entry having the same key is replaced.
        """
        remaining = frozenset(
            e
            for e in self.entries
            if e.key != entry.key
        )

        return Configuration(
            remaining | frozenset((entry,))
        )

    def remove(
        self,
        key: ConfigurationKey,
    ) -> "Configuration":
        """
        Returns a new configuration without the supplied key.
        """
        return Configuration(
            frozenset(
                e
                for e in self.entries
                if e.key != key
            )
        )

    @property
    def display_name(self) -> str:
        return f"{self.count} Configuration Entries"

    @property
    def display_text(self) -> str:
        return ", ".join(
            sorted(
                entry.identifier
                for entry in self.entries
            )
        )

    def __contains__(
        self,
        key: ConfigurationKey,
    ) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[ConfigurationEntry]:
        return iter(
            sorted(
                self.entries,
                key=lambda entry: entry.identifier,
            )
        )

    def __bool__(self) -> bool:
        return not self.is_empty

    def __str__(self) -> str:
        return self.display_text

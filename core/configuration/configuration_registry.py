from __future__ import annotations

"""
SanskritAI
==========

Configuration Registry

Defines the canonical immutable registry of configuration
profiles.

A ConfigurationRegistry provides centralized registration and
lookup of ConfigurationProfile objects. It does not manage
individual configuration entries directly.

Architecture
------------

Registry
      │
      ▼
ConfigurationRegistry
      │
      └── ConfigurationProfile

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from collections.abc import Iterator

from SanskritAI.core.configuration.configuration_profile import (
    ConfigurationProfile,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationRegistry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable registry of configuration profiles.
    """

    profiles: frozenset[ConfigurationProfile] = field(
        default_factory=frozenset
    )

    @property
    def count(self) -> int:
        """
        Returns the number of registered profiles.
        """
        return len(self.profiles)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the registry contains no profiles.
        """
        return self.count == 0

    def register(
        self,
        profile: ConfigurationProfile,
    ) -> "ConfigurationRegistry":
        """
        Returns a new registry containing the supplied profile.

        Existing profiles having the same identifier are replaced.
        """
        remaining = frozenset(
            p
            for p in self.profiles
            if p.identifier != profile.identifier
        )

        return ConfigurationRegistry(
            remaining | frozenset((profile,))
        )

    def unregister(
        self,
        identifier: str,
    ) -> "ConfigurationRegistry":
        """
        Returns a new registry with the supplied profile removed.
        """
        normalized = identifier.strip()

        return ConfigurationRegistry(
            frozenset(
                profile
                for profile in self.profiles
                if profile.identifier != normalized
            )
        )

    def lookup(
        self,
        identifier: str,
    ) -> ConfigurationProfile | None:
        """
        Looks up a configuration profile by its identifier.
        """
        normalized = identifier.strip()

        for profile in self.profiles:
            if profile.identifier == normalized:
                return profile

        return None

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether a configuration profile exists.
        """
        return self.lookup(identifier) is not None

    @property
    def display_name(self) -> str:
        return f"{self.count} Configuration Profiles"

    @property
    def display_text(self) -> str:
        return ", ".join(
            sorted(
                profile.identifier
                for profile in self.profiles
            )
        )

    def __contains__(
        self,
        identifier: str,
    ) -> bool:
        return self.contains(identifier)

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[ConfigurationProfile]:
        return iter(
            sorted(
                self.profiles,
                key=lambda profile: profile.identifier,
            )
        )

    def __bool__(self) -> bool:
        return not self.is_empty

    def __str__(self) -> str:
        return self.display_text

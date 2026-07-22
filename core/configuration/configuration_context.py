from __future__ import annotations

"""
SanskritAI
==========

Configuration Context

Defines the immutable active runtime configuration context.

A ConfigurationContext represents the effective configuration
available to a runtime component after configuration profiles
have been selected and configuration sources have been resolved.

Unlike ConfigurationProfile, which describes a component's
configuration, ConfigurationContext represents the configuration
currently active within a particular execution scope.

Typical examples include:

- Parser execution
- Dictionary lookup
- AI inference
- Corpus import
- Django request
- Background worker

Architecture
------------

ValueObject
      │
      ▼
ConfigurationContext
      │
      └── ConfigurationProfile

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.configuration.configuration_entry import ConfigurationEntry
from SanskritAI.core.configuration.configuration_key import ConfigurationKey
from SanskritAI.core.configuration.configuration_profile import (
    ConfigurationProfile,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime configuration context.
    """

    profile: ConfigurationProfile

    @property
    def identifier(self) -> str:
        """
        Returns the underlying profile identifier.
        """
        return self.profile.identifier

    @property
    def configuration(self):
        """
        Returns the active configuration.
        """
        return self.profile.configuration

    def contains(
        self,
        key: ConfigurationKey,
    ) -> bool:
        """
        Determines whether the supplied configuration key exists.
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
        return self.profile.display_name

    @property
    def display_text(self) -> str:
        return self.profile.display_text

    @property
    def display_description(self) -> str:
        return self.profile.display_description

    def __str__(self) -> str:
        return self.display_text

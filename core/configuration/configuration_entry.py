from __future__ import annotations

"""
SanskritAI
==========

Configuration Entry

Defines the canonical immutable configuration record.

A ConfigurationEntry associates a configuration key with its
typed value and descriptive metadata.

Unlike raw dictionaries, ConfigurationEntry provides a strongly
typed, immutable representation that can be consumed uniformly
by configuration providers, registries, loaders, and runtime
components.

Architecture
------------

ValueObject
      │
      ▼
ConfigurationEntry
      │
      ├── ConfigurationKey
      ├── ConfigurationValue
      └── ConfigurationMetadata

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.configuration.configuration_key import ConfigurationKey
from SanskritAI.core.configuration.configuration_metadata import (
    ConfigurationMetadata,
)
from SanskritAI.core.configuration.configuration_value import (
    ConfigurationValue,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationEntry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable configuration entry.
    """

    key: ConfigurationKey

    value: ConfigurationValue

    metadata: ConfigurationMetadata = ConfigurationMetadata()

    enabled: bool = True

    @property
    def identifier(self) -> str:
        """
        Returns the canonical identifier.
        """
        return self.key.identifier

    @property
    def has_default(self) -> bool:
        """
        Returns True if a default value is defined.
        """
        return self.metadata.has_default

    @property
    def default_value(self) -> ConfigurationValue | None:
        """
        Returns the configured default value, if any.
        """
        return self.metadata.default_value

    @property
    def is_required(self) -> bool:
        """
        Indicates whether this configuration is required.
        """
        return self.metadata.required

    @property
    def is_read_only(self) -> bool:
        """
        Indicates whether this configuration is read-only.
        """
        return self.metadata.read_only

    @property
    def is_deprecated(self) -> bool:
        """
        Indicates whether this configuration has been
        deprecated.
        """
        return self.metadata.deprecated

    @property
    def display_name(self) -> str:
        return self.key.display_name

    @property
    def display_text(self) -> str:
        return f"{self.key} = {self.value}"

    @property
    def display_description(self) -> str:
        return self.metadata.display_description

    def with_value(
        self,
        value: ConfigurationValue,
    ) -> "ConfigurationEntry":
        """
        Returns a new entry with the supplied value.
        """
        return ConfigurationEntry(
            key=self.key,
            value=value,
            metadata=self.metadata,
            enabled=self.enabled,
        )

    def enable(self) -> "ConfigurationEntry":
        """
        Returns an enabled configuration entry.
        """
        return ConfigurationEntry(
            key=self.key,
            value=self.value,
            metadata=self.metadata,
            enabled=True,
        )

    def disable(self) -> "ConfigurationEntry":
        """
        Returns a disabled configuration entry.
        """
        return ConfigurationEntry(
            key=self.key,
            value=self.value,
            metadata=self.metadata,
            enabled=False,
        )

    def __str__(self) -> str:
        return self.display_text

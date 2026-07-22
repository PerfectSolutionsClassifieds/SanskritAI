from __future__ import annotations

"""
SanskritAI
==========

Configuration Metadata

Defines immutable descriptive metadata associated with a
configuration entry.

ConfigurationMetadata contains information describing a
configuration option rather than its runtime value.

Typical metadata includes:

- description
- default value
- required flag
- read-only flag
- deprecated flag
- version introduced
- source information

The metadata object intentionally remains lightweight while
providing a stable foundation for future schema validation,
documentation generation, configuration editors, and runtime
inspection.

Architecture
------------

ValueObject
      │
      ▼
ConfigurationMetadata
      │
      ▼
ConfigurationEntry

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.core.configuration.configuration_value import (
    ConfigurationValue,
)
from SanskritAI.core.configuration.configuration_source import (
    ConfigurationSource,
)

@dataclass(frozen=True, slots=True)
class ConfigurationMetadata(ValueObject, Immutable, Displayable):
    """
    Immutable metadata describing a configuration entry.
    """

    description: str = ""

    required: bool = False

    read_only: bool = False

    deprecated: bool = False

    # default_value: str | None = None
    default_value: ConfigurationValue | None = None


    introduced_in: str | None = None

    # source: str | None = None
    source: ConfigurationSource | None = None

    @property
    def has_default(self) -> bool:
        """
        Returns True if a default value has been defined.
        """
        return self.default_value is not None

    @property
    def is_mutable(self) -> bool:
        """
        Returns True if the configuration is writable.
        """
        return not self.read_only

    @property
    def display_name(self) -> str:
        return "Configuration Metadata"

    @property
    def display_text(self) -> str:
        if self.description:
            return self.description
        return "Configuration metadata"

    @property
    def display_description(self) -> str:
        return self.display_text

    def __str__(self) -> str:
        return self.display_text

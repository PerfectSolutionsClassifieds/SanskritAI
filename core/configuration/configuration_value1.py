from __future__ import annotations

"""
SanskritAI
==========

Configuration Value

Defines the canonical immutable wrapper for configuration
values.

Unlike raw Python values, ConfigurationValue preserves both the
value and its runtime type, providing a foundation for future
validation, schema enforcement, serialization, and configuration
loading.

Typical values include:

- bool
- int
- float
- str
- tuple
- frozenset
- None

Architecture
------------

ValueObject
      │
      ▼
ConfigurationValue
      │
      ▼
ConfigurationEntry

Version
-------
v0.6.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationValue(ValueObject, Immutable, Displayable):
    """
    Immutable typed configuration value.
    """

    value: Any

    @property
    def value_type(self) -> type:
        """
        Returns the runtime type of the wrapped value.
        """
        return type(self.value)

    @property
    def type_name(self) -> str:
        """
        Returns the simple runtime type name.
        """
        return self.value_type.__name__

    @property
    def is_none(self) -> bool:
        """
        Returns True if the wrapped value is None.
        """
        return self.value is None

    @property
    def display_name(self) -> str:
        return self.type_name

    @property
    def display_text(self) -> str:
        return repr(self.value)

    @property
    def display_description(self) -> str:
        return f"Configuration value of type '{self.type_name}'."

    def is_instance_of(
        self,
        expected_type: type,
    ) -> bool:
        """
        Determines whether the wrapped value is an instance of
        the supplied type.
        """
        return isinstance(self.value, expected_type)

    def unwrap(self) -> Any:
        """
        Returns the underlying Python value.
        """
        return self.value

    def __str__(self) -> str:
        return repr(self.value)

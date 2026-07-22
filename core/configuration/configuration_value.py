from __future__ import annotations

"""
SanskritAI
==========

Configuration Value

Defines the canonical immutable wrapper for configuration
values.

Unlike raw Python values, ConfigurationValue preserves both the
value and its runtime type, providing a foundation for future
validation, schema enforcement, serialization, configuration
loading, and dependency injection.

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
ConfigurationValue[T]
      │
      ▼
ConfigurationEntry

Version
-------
v0.6.0
"""

from dataclasses import dataclass
from collections.abc import Collection
from typing import Any
from typing import Generic
from typing import TypeVar

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ConfigurationValue(
    ValueObject,
    Immutable,
    Displayable,
    Generic[T],
):
    """
    Immutable typed configuration value.
    """

    value: T

    @property
    def type(self) -> type:
        """
        Returns the runtime type of the wrapped value.
        """
        return type(self.value)

    @property
    def type_name(self) -> str:
        """
        Returns the runtime type name.
        """
        return self.type.__name__

    @property
    def is_none(self) -> bool:
        """
        Returns True if the wrapped value is None.
        """
        return self.value is None

    @property
    def is_scalar(self) -> bool:
        """
        Returns True if the wrapped value represents a scalar.
        """
        return not self.is_collection

    @property
    def is_collection(self) -> bool:
        """
        Returns True if the wrapped value is a collection.

        Strings and bytes are treated as scalar values.
        """
        return (
            isinstance(self.value, Collection)
            and not isinstance(self.value, (str, bytes, bytearray))
        )

    @property
    def display_name(self) -> str:
        return self.type_name

    @property
    def display_text(self) -> str:
        return repr(self.value)

    @property
    def display_description(self) -> str:
        return (
            f"Configuration value of type "
            f"'{self.type_name}'."
        )

    def is_instance_of(
        self,
        expected_type: type,
    ) -> bool:
        """
        Determines whether the wrapped value is an instance of
        the supplied type.
        """
        return isinstance(self.value, expected_type)

    def unwrap(self) -> T:
        """
        Returns the underlying Python value.
        """
        return self.value

    def __str__(self) -> str:
        return repr(self.value)

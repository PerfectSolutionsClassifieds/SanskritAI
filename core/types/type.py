from __future__ import annotations

"""
SanskritAI
==========

Generic Type

Defines the canonical immutable base class for typed value
objects.

Version
-------
v0.7.0
"""

from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Type(
    ValueObject,
    Immutable,
    Displayable,
    Generic[T],
):
    """
    Generic immutable typed value.
    """

    value: T

    @property
    def identifier(self) -> str:
        return str(self.value)

    @property
    def display_name(self) -> str:
        return str(self.value)

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return f"{type(self).__name__}: {self.value}"

    def __str__(self) -> str:
        return str(self.value)

from __future__ import annotations

"""
SanskritAI
==========

IntegerType

Canonical immutable integer wrapper.

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class IntegerType(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable integer wrapper.
    """

    value: int

    @property
    def identifier(self) -> str:
        return str(self.value)

    @property
    def display_name(self) -> str:
        return str(self.value)

    @property
    def display_text(self) -> str:
        return str(self.value)

    @property
    def display_description(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

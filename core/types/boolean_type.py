from __future__ import annotations

"""
SanskritAI
==========

BooleanType

Canonical immutable boolean wrapper.

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class BooleanType(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable boolean wrapper.
    """

    value: bool

    @property
    def identifier(self) -> str:
        return str(self.value).lower()

    @property
    def display_name(self) -> str:
        return "True" if self.value else "False"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.display_name

    def __bool__(self) -> bool:
        return self.value

    def __str__(self) -> str:
        return self.identifier

from __future__ import annotations

"""
SanskritAI
==========

StringType

Canonical immutable wrapper around a string.

Semantic string value objects throughout SanskritAI should
inherit from StringType rather than directly wrapping `str`.

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class StringType(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable string wrapper.
    """

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value.strip())

    @property
    def identifier(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        return self.value

    @property
    def display_text(self) -> str:
        return self.value

    @property
    def display_description(self) -> str:
        return self.value

    @property
    def is_empty(self) -> bool:
        return self.value == ""

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)

from __future__ import annotations

"""
SanskritAI
==========

Vacana

Represents the canonical grammatical number in Sanskrit.

Relationship
------------

MorphologicalFeatures
    └── Vacana

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Vacana(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable grammatical number.
    """

    identifier: int

    sanskrit_name: str

    english_name: str

    abbreviation: str = ""

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.sanskrit_name

    @property
    def display_text(self) -> str:
        if self.english_name:
            return (
                f"{self.sanskrit_name}"
                f" ({self.english_name})"
            )
        return self.sanskrit_name

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Location

Defines the canonical immutable representation of a location.

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.location.location_kind import LocationKind
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Location(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable location.
    """

    value: str

    kind: LocationKind

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "Location cannot be empty."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

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
        return (
            f"{self.kind.display_name} location."
        )

    def __str__(self) -> str:
        return self.value

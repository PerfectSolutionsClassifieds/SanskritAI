from __future__ import annotations

"""
SanskritAI
==========

Version Constraint

Defines immutable version constraints.

Examples
--------

>=1.0.0

==0.7.0

~=2.1

<3.0

Architecture
------------

ValueObject
      │
      ▼
VersionConstraint

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class VersionConstraint(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable version constraint.
    """

    expression: str

    def __post_init__(self) -> None:
        normalized = self.expression.strip()

        if not normalized:
            raise ValueError(
                "Version constraint cannot be empty."
            )

        object.__setattr__(
            self,
            "expression",
            normalized,
        )

    @property
    def identifier(self) -> str:
        return self.expression

    @property
    def display_name(self) -> str:
        return self.expression

    @property
    def display_text(self) -> str:
        return self.expression

    @property
    def display_description(self) -> str:
        return (
            f"Version constraint '{self.expression}'."
        )

    def __str__(self) -> str:
        return self.expression

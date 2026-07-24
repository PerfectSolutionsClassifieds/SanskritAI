from __future__ import annotations

"""
SanskritAI
==========

Resource Identifier

Defines the canonical immutable identifier of a resource.

A ResourceId uniquely identifies a resource independently of its
physical storage location.

Examples
--------

amarakosha

mahabharata_pdf

dictionary_index

embeddings

Architecture
------------

ValueObject
      │
      ▼
ResourceId
      │
      ▼
ResourceMetadata

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResourceId(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable resource identifier.
    """

    name: str

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Resource identifier cannot be empty."
            )

        object.__setattr__(
            self,
            "name",
            normalized,
        )

    @property
    def identifier(self) -> str:
        """
        Returns the canonical resource identifier.
        """
        return self.name

    @property
    def display_name(self) -> str:
        return self.name.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            f"Resource '{self.display_name}'."
        )

    def matches(
        self,
        identifier: str,
    ) -> bool:
        return (
            self.name ==
            identifier.strip().lower()
        )

    def __str__(self) -> str:
        return self.identifier

from __future__ import annotations

"""
SanskritAI
==========

Grammatical Category Collection

Immutable collection of grammatical categories.

This collection forms the canonical container for Sanskrit
grammatical categories and is reused throughout the
Morphology Kernel.

Examples
--------

Vibhaktis

Vacanas

Lingas

Lakaras

Future relationships
--------------------

MorphologicalFeatures
        │
        └── GrammaticalCategoryCollection

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.morphology.grammatical_category import (
    GrammaticalCategory,
)


@dataclass(frozen=True, slots=True)
class GrammaticalCategoryCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of grammatical categories.
    """

    categories: tuple[
        GrammaticalCategory,
        ...
    ] = field(default_factory=tuple)

    def __iter__(self) -> Iterator[GrammaticalCategory]:
        return iter(self.categories)

    def __len__(self) -> int:
        return len(self.categories)

    def __getitem__(
        self,
        index: int,
    ) -> GrammaticalCategory:
        return self.categories[index]

    @property
    def is_empty(self) -> bool:
        return len(self.categories) == 0

    @property
    def count(self) -> int:
        return len(self.categories)

    @property
    def display_name(self) -> str:
        return "Grammatical Categories"

    @property
    def display_text(self) -> str:
        return f"{self.count} Categories"

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of grammatical "
            "categories."
        )

    def __str__(self) -> str:
        return self.display_text

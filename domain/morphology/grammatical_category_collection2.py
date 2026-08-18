from __future__ import annotations

"""
SanskritAI
==========

Grammatical Category Collection

Immutable collection of canonical grammatical categories.

Version
-------
v2.0.0
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

    items: tuple[
        GrammaticalCategory,
        ...
    ] = field(default_factory=tuple)

    def __iter__(self) -> Iterator[GrammaticalCategory]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(
        self,
        index: int,
    ) -> GrammaticalCategory:
        return self.items[index]

    def __contains__(
        self,
        category: GrammaticalCategory,
    ) -> bool:
        return category in self.items

    @property
    def count(self) -> int:
        return len(self.items)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(
        self,
    ) -> GrammaticalCategory | None:
        return self.items[0] if self.items else None

    @property
    def last(
        self,
    ) -> GrammaticalCategory | None:
        return self.items[-1] if self.items else None

    def find(
        self,
        identifier: str,
    ) -> GrammaticalCategory | None:

        for item in self.items:
            if item.identifier == identifier:
                return item
        return None

    @property
    def display_name(self) -> str:
        return "Grammatical Categories"

    @property
    def display_text(self) -> str:
        return f"{self.count} Categories"

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of canonical "
            "grammatical categories."
        )

    def __str__(self) -> str:
        return self.display_text

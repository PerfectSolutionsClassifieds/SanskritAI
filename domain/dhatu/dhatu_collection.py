from __future__ import annotations

"""
SanskritAI
==========

Dhatu Collection

Defines the immutable collection of Dhatu objects.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.dhatu.dhatu import Dhatu


@dataclass(frozen=True, slots=True)
class DhatuCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of Dhatu objects.
    """

    dhatus: tuple[Dhatu, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Dhatu Collection"

    @property
    def display_text(self) -> str:
        return f"{len(self.dhatus)} Dhatus"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Sanskrit verbal roots."

    @property
    def count(self) -> int:
        return len(self.dhatus)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> Dhatu | None:
        if self.is_empty:
            return None
        return self.dhatus[0]

    def add(self, dhatu: Dhatu) -> "DhatuCollection":
        return DhatuCollection(dhatus=self.dhatus + (dhatu,))

    def extend(self, other: "DhatuCollection") -> "DhatuCollection":
        return DhatuCollection(dhatus=self.dhatus + other.dhatus)

    def get_by_root(self, root: str) -> Dhatu | None:
        for dhatu in self.dhatus:
            if dhatu.root == root:
                return dhatu
        return None

    def __iter__(self) -> Iterator[Dhatu]:
        return iter(self.dhatus)

    def __len__(self) -> int:
        return len(self.dhatus)

    def __getitem__(self, index: int) -> Dhatu:
        return self.dhatus[index]

    def __str__(self) -> str:
        return self.display_text

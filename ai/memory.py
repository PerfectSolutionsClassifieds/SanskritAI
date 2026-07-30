from __future__ import annotations

"""
SanskritAI
==========

Memory

Defines an immutable semantic memory snapshot.

A Memory represents the contextual knowledge available to
a reasoning session. It contains immutable knowledge items
without prescribing how they are stored or retrieved.

Concrete memory stores (vector databases, SQL databases,
knowledge graphs, caches, etc.) belong to higher layers.

Architecture
------------

Memory
    │
    ▼
ReasoningContext
    │
    ▼
Reasoner

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Memory(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic memory.

    Represents the contextual knowledge supplied to a
    reasoning session.
    """

    identifier: str

    name: str

    items: tuple[object, ...] = field(
        default_factory=tuple,
    )

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    @property
    def has_items(self) -> bool:
        return not self.is_empty

    def add_item(
        self,
        item: object,
    ) -> "Memory":
        """
        Returns a new Memory instance containing the supplied
        item.
        """
        return Memory(
            identifier=self.identifier,
            name=self.name,
            items=self.items + (item,),
            description=self.description,
        )

    def __iter__(self) -> Iterator[object]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return self.display_text

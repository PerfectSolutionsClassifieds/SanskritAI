from __future__ import annotations

"""
SanskritAI
==========

Indexed Collection

Purpose
-------

Provides a reusable immutable collection whose primary
access mechanism is one or more indexes.

An IndexedCollection owns

    • immutable items

    • immutable indexes

Concrete implementations include

    • PaninianSutraIndex

    • DhatuIndex

    • DictionaryIndex

    • SemanticIndex

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Generic
from typing import Iterator
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class IndexedCollection(
    Generic[T],
):
    """
    Immutable indexed collection.
    """

    items: tuple[T, ...] = ()

    # ---------------------------------------------------------
    # Basic information
    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:
        return len(self.items)

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.count == 0

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    def contains(
        self,
        item: T,
    ) -> bool:
        return item in self.items

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __contains__(
        self,
        item: T,
    ) -> bool:
        return self.contains(item)

    def __len__(
        self,
    ) -> int:
        return self.count

    def __iter__(
        self,
    ) -> Iterator[T]:
        yield from self.items

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "items": self.count,
        }

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"({self.count} items)"
        )

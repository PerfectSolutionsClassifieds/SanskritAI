from __future__ import annotations

"""
SanskritAI
==========

Immutable Index

Purpose
-------

Provides the canonical immutable lookup structure used
throughout SanskritAI.

An ImmutableIndex maps a key to one or more immutable
objects while preventing mutation after construction.

This class is intentionally domain-independent.

Future users
------------

• PaninianSutraIndex

• DhatuIndex

• PratyayaIndex

• DictionaryIndex

• KnowledgeGraphIndex

• ChandasIndex

• SemanticIndex

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass(frozen=True, slots=True)
class ImmutableIndex(
    Generic[K, V],
):
    """
    Immutable key → tuple[value] index.
    """

    _mapping: dict[K, tuple[V, ...]] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    @classmethod
    def build(
        cls,
        items: Iterable[V],
        *,
        key_selector: Callable[[V], K],
    ) -> "ImmutableIndex[K, V]":
        """
        Builds an immutable index.
        """

        buckets: dict[K, list[V]] = {}

        for item in items:

            key = key_selector(item)

            buckets.setdefault(
                key,
                [],
            ).append(item)

        frozen = {

            key: tuple(values)

            for key, values

            in buckets.items()

        }

        return cls(
            _mapping=frozen,
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        key: K,
    ) -> tuple[V, ...]:

        return self._mapping.get(
            key,
            (),
        )

    def first(
        self,
        key: K,
    ) -> V | None:

        values = self.get(key)

        if values:
            return values[0]

        return None

    def contains(
        self,
        key: K,
    ) -> bool:

        return key in self._mapping

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    @property
    def keys(
        self,
    ) -> tuple[K, ...]:

        return tuple(
            sorted(
                self._mapping.keys(),
            )
        )

    @property
    def values(
        self,
    ) -> tuple[V, ...]:

        collected: list[V] = []

        for bucket in self._mapping.values():

            collected.extend(bucket)

        return tuple(collected)

    @property
    def item_count(
        self,
    ) -> int:

        return len(
            self.values,
        )

    @property
    def key_count(
        self,
    ) -> int:

        return len(
            self._mapping,
        )

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __contains__(
        self,
        key: K,
    ) -> bool:

        return self.contains(key)

    def __len__(
        self,
    ) -> int:

        return self.key_count

    def __iter__(
        self,
    ) -> Iterator[K]:

        yield from self.keys

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "keys": self.key_count,

            "items": self.item_count,

        }

    def __str__(
        self,
    ) -> str:

        return (
            "ImmutableIndex("
            f"{self.key_count} keys, "
            f"{self.item_count} items)"
        )

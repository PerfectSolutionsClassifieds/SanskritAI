from __future__ import annotations

"""
SanskritAI
==========

Multi Index

Purpose
-------

Provides an immutable collection of named
ImmutableIndex objects.

Rather than representing one particular index,
MultiIndex groups multiple orthogonal indexes over
the same immutable collection.

Examples
--------

PaninianSutraIndex

    sutra_number

    adhyaya

    pada

    category

    operation

    behaviour

DhatuIndex

    dhatu

    gana

    pada

DictionaryIndex

    headword

    language

    source

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any
from typing import Iterator

from SanskritAI.core.indexing.immutable_index import (
    ImmutableIndex,
)


@dataclass(frozen=True, slots=True)
class MultiIndex:
    """
    Immutable registry of named indexes.
    """

    indexes: dict[str, ImmutableIndex[Any, Any]]

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get_index(
        self,
        name: str,
    ) -> ImmutableIndex[Any, Any]:
        """
        Returns the named index.

        Raises
        ------
        KeyError
            If the index does not exist.
        """

        try:
            return self.indexes[name]

        except KeyError as exc:
            raise KeyError(
                f"Unknown index '{name}'."
            ) from exc

    def contains_index(
        self,
        name: str,
    ) -> bool:
        """
        Returns True if the named index exists.
        """

        return name in self.indexes

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    @property
    def names(
        self,
    ) -> tuple[str, ...]:
        """
        Returns all index names.
        """

        return tuple(
            sorted(
                self.indexes.keys(),
            )
        )

    @property
    def count(
        self,
    ) -> int:
        """
        Number of indexes.
        """

        return len(
            self.indexes,
        )

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return self.contains_index(
            name,
        )

    def __len__(
        self,
    ) -> int:
        return self.count

    def __iter__(
        self,
    ) -> Iterator[str]:
        yield from self.names

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Returns summary information.
        """

        return {
            "index_count": self.count,
            "indexes": self.names,
        }

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.count} indexes)"
        )

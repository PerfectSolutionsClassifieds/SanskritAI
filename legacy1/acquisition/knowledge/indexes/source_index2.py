from __future__ import annotations

"""
SanskritAI
==========

Source Index

Purpose
-------
Indexes Dictionary Senses by CanonicalSource.

The Reader UI typically asks:

    "Show every lexical sense originating from
     Monier-Williams."

rather than retrieving the CanonicalSource object.

Architecture
------------

CanonicalSource.source_id
            │
            ▼
tuple[CanonicalDictionarySense]

Version
-------
2.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


@dataclass(slots=True)
class SourceIndex:

    _index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def add(
        self,
        source: CanonicalSource,
        sense: CanonicalDictionarySense,
    ) -> None:

        bucket = self._index.setdefault(
            source.source_id,
            [],
        )

        bucket.append(
            sense,
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        source_id: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...
    ]:

        return tuple(

            self._index.get(
                source_id,
                [],
            )

        )

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._index.clear()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def source_count(
        self,
    ) -> int:

        return len(
            self._index,
        )

    def summary(
        self,
    ) -> dict:

        return {

            "sources": self.source_count,

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __contains__(
        self,
        source_id: str,
    ) -> bool:

        return source_id in self._index

    def __len__(
        self,
    ) -> int:

        return self.source_count

    def __iter__(
        self,
    ):

        yield from sorted(
            self._index.keys(),
        )

    def __str__(
        self,
    ) -> str:

        return (

            "SourceIndex("

            f"{self.source_count} sources)"

        )

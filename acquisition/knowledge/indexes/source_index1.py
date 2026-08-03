from __future__ import annotations

"""
SanskritAI
==========

Source Index

Purpose
-------
Indexes canonical lexical sources available inside the
Canonical Knowledge Repository.

Unlike SourceRegistry, which merely stores CanonicalSource
objects, SourceIndex provides efficient lookup by various
identifiers.

Architecture
------------

CanonicalKnowledgeRepository
            │
            ▼
        SourceIndex
            │
            ▼
      CanonicalSource

Responsibilities
----------------

• Index canonical sources

• Lookup by source id

• Lookup by canonical name

• Lookup by short name

• Enumerate sources

• Prepare for future source ranking and prioritization

Examples
--------

Monier-Williams

Apte

Amarakośa

Śabdakalpadruma

Vācaspatyam

Dhātupāṭha

Gaṇapāṭha

Uṇādi

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


@dataclass(slots=True)
class SourceIndex:
    """
    Canonical searchable source index.
    """

    _sources: dict[
        str,
        CanonicalSource,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _name_index: dict[
        str,
        CanonicalSource,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _short_name_index: dict[
        str,
        CanonicalSource,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Index Construction
    # ---------------------------------------------------------

    def add(
        self,
        source: CanonicalSource,
    ) -> None:
        """
        Adds one canonical source.
        """

        self._sources.setdefault(
            source.source_id,
            source,
        )

        self._name_index.setdefault(
            source.name,
            source,
        )

        self._short_name_index.setdefault(
            source.short_name,
            source,
        )

    def build(
        self,
        sources: tuple[
            CanonicalSource,
            ...,
        ],
    ) -> None:
        """
        Rebuilds the complete source index.
        """

        self.clear()

        for source in sources:

            self.add(
                source,
            )

    def clear(
        self,
    ) -> None:

        self._sources.clear()

        self._name_index.clear()

        self._short_name_index.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        source_id: str,
    ) -> CanonicalSource | None:

        return self._sources.get(
            source_id,
        )

    def lookup_name(
        self,
        name: str,
    ) -> CanonicalSource | None:

        return self._name_index.get(
            name,
        )

    def lookup_short_name(
        self,
        short_name: str,
    ) -> CanonicalSource | None:

        return self._short_name_index.get(
            short_name,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[
        CanonicalSource,
        ...,
    ]:

        return tuple(

            sorted(

                self._sources.values(),

                key=lambda x: x.display_name,

            )

        )

    @property
    def source_ids(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                self._sources.keys(),
            )
        )

    @property
    def source_names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                self._name_index.keys(),
            )
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "sources": len(
                self,
            ),

            "canonical_names": len(
                self._name_index,
            ),

            "short_names": len(
                self._short_name_index,
            ),

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._sources,
        )

    def __iter__(
        self,
    ):

        yield from self.all()

    def __contains__(
        self,
        source_id: str,
    ) -> bool:

        return source_id in self._sources

    def __str__(
        self,
    ) -> str:

        return (
            "SourceIndex("
            f"{len(self)} indexed sources)"
        )

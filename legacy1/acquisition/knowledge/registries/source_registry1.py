from __future__ import annotations

"""
SanskritAI
==========

Source Registry

Purpose
-------
Canonical in-memory registry of all CanonicalSource
objects loaded into the Canonical Knowledge Repository.

A CanonicalSource represents an authoritative lexical,
grammatical, or textual resource.

Examples
--------

    • Monier–Williams

    • Apte

    • Amarakośa

    • Śabdakalpadruma

    • Vācaspatyam

    • Dhātupāṭha

    • Gaṇapāṭha

Architecture
------------

Acquisition Pipelines
        │
        ▼
CanonicalSource
        │
        ▼
SourceRegistry
        │
        ▼
CanonicalKnowledgeRepository

Responsibilities
----------------

• Register canonical sources

• Lookup sources

• Enumerate sources

• Prevent duplicate registrations

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
class SourceRegistry:
    """
    Registry of CanonicalSource objects.
    """

    _sources: dict[
        str,
        CanonicalSource,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        source: CanonicalSource,
    ) -> None:
        """
        Registers one canonical source.

        Duplicate identifiers are ignored.
        """

        if source.source_id in self._sources:
            return

        self._sources[
            source.source_id
        ] = source

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

    def lookup_by_name(
        self,
        name: str,
    ) -> CanonicalSource | None:
        """
        Lookup by canonical source name.
        """

        for source in self._sources.values():

            if source.name == name:

                return source

        return None

    def lookup_by_short_name(
        self,
        short_name: str,
    ) -> CanonicalSource | None:
        """
        Lookup by abbreviated source name.
        """

        for source in self._sources.values():

            if source.short_name == short_name:

                return source

        return None

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

            "ids": self.source_ids,

        }

    # ---------------------------------------------------------
    # Python protocol
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

        return (
            source_id
            in self._sources
        )

    def __str__(
        self,
    ) -> str:

        return (

            "SourceRegistry("

            f"{len(self)} sources)"

        )

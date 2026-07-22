
from __future__ import annotations

"""
SanskritAI
==========

Source Catalog

A collection of CorpusSource objects known to SanskritAI.

The SourceCatalog is an in-memory collection responsible for:

    • Storing registered corpus sources
    • Looking up sources
    • Enumerating sources
    • Filtering sources
    • Preventing duplicate registrations

The catalog intentionally contains no downloading,
validation, storage, or persistence logic.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from collections.abc import Iterator
from typing import Iterable

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType


class SourceCatalog:
    """
    In-memory collection of CorpusSource objects.
    """

    def __init__(
        self,
        sources: Iterable[CorpusSource] | None = None,
    ) -> None:
        self._sources: dict[str, CorpusSource] = {}

        if sources:
            for source in sources:
                self.add(source)

    # ------------------------------------------------------------------
    # Collection API
    # ------------------------------------------------------------------

    def add(
        self,
        source: CorpusSource,
    ) -> None:
        """
        Adds a source to the catalog.

        Raises
        ------
        ValueError
            If a source with the same source_id already exists.
        """
        if source.source_id in self._sources:
            raise ValueError(
                f"Duplicate source_id: {source.source_id!r}"
            )

        self._sources[source.source_id] = source

    def remove(
        self,
        source_id: str,
    ) -> CorpusSource:
        """
        Removes a source from the catalog.

        Raises
        ------
        KeyError
            If the source does not exist.
        """
        return self._sources.pop(source_id)

    def clear(self) -> None:
        """Removes all registered sources."""
        self._sources.clear()

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        source_id: str,
    ) -> CorpusSource | None:
        """
        Returns the source or None.
        """
        return self._sources.get(source_id)

    def require(
        self,
        source_id: str,
    ) -> CorpusSource:
        """
        Returns the source.

        Raises
        ------
        KeyError
            If the source is not present.
        """
        return self._sources[source_id]

    def contains(
        self,
        source_id: str,
    ) -> bool:
        """
        Returns True if the source exists.
        """
        return source_id in self._sources

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def by_type(
        self,
        source_type: SourceType,
    ) -> list[CorpusSource]:
        """
        Returns all sources of the given type.
        """
        return [
            source
            for source in self._sources.values()
            if source.source_type == source_type
        ]

    def by_status(
        self,
        status: SourceStatus,
    ) -> list[CorpusSource]:
        """
        Returns all sources having the specified status.
        """
        return [
            source
            for source in self._sources.values()
            if source.status == status
        ]

    def enabled(self) -> list[CorpusSource]:
        """
        Returns all enabled sources.

        A source is considered enabled if its status
        is not terminal.
        """
        return [
            source
            for source in self._sources.values()
            if not source.status.is_terminal
        ]

    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------

    def ids(self) -> list[str]:
        """
        Returns source identifiers.
        """
        return sorted(self._sources.keys())

    def values(self) -> list[CorpusSource]:
        """
        Returns all sources.
        """
        return list(self._sources.values())

    def items(
        self,
    ) -> list[tuple[str, CorpusSource]]:
        """
        Returns (source_id, source) pairs.
        """
        return list(self._sources.items())

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def size(self) -> int:
        """Number of registered sources."""
        return len(self._sources)

    @property
    def is_empty(self) -> bool:
        """Returns True if the catalog is empty."""
        return not self._sources

    # ------------------------------------------------------------------
    # Python Protocols
    # ------------------------------------------------------------------

    def __contains__(
        self,
        source_id: object,
    ) -> bool:
        if not isinstance(source_id, str):
            return False

        return source_id in self._sources

    def __len__(self) -> int:
        return len(self._sources)

    def __iter__(self) -> Iterator[CorpusSource]:
        return iter(self._sources.values())

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"SourceCatalog("
            f"sources={len(self._sources)})"
        )

from __future__ import annotations

"""
SanskritAI
==========

Default Source Repository

In-memory implementation of SourceRepository.

This repository deliberately contains no file-system,
network, parser, downloader, or acquisition logic.

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.repositories.source_repository import (
    SourceRepository,
)


@dataclass(
    slots=True,
)
class DefaultSourceRepository(
    SourceRepository,
):
    """
    Canonical in-memory source repository.
    """

    _sources: dict[str, CorpusSource] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Source Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "In-memory repository for canonical "
            "corpus-source metadata."
        )

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> CorpusSource | None:
        """
        Returns a source by identifier.
        """
        return self._sources.get(identifier)

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Returns True when the identifier is registered.
        """
        return identifier in self._sources

    def all(self) -> tuple[CorpusSource, ...]:
        """
        Returns all sources as an immutable snapshot.

        Dictionary insertion order is preserved.
        """
        return tuple(
            self._sources.values()
        )

    # ---------------------------------------------------------
    # Mutation
    # ---------------------------------------------------------

    def add(
        self,
        source: CorpusSource,
    ) -> CorpusSource:
        """
        Registers a source.

        Duplicate identifiers are rejected.
        """
        if self.exists(source.identifier):
            raise ValueError(
                "A source with identifier "
                f"'{source.identifier}' already exists."
            )

        self._sources[source.identifier] = source

        return source

    def remove(
        self,
        identifier: str,
    ) -> CorpusSource | None:
        """
        Removes and returns a source.
        """
        return self._sources.pop(
            identifier,
            None,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Removes all registered sources.
        """
        self._sources.clear()

    def __iter__(self):
        return iter(self.all())

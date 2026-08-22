from __future__ import annotations

"""
SanskritAI
==========

Default Source Repository

Canonical in-memory repository implementation for CorpusSource.

Responsibilities
----------------

- Register CorpusSource instances.
- Prevent duplicate source identifiers.
- Retrieve sources by source_id.
- Determine whether a source exists.
- Return an immutable snapshot of registered sources.
- Remove sources.
- Clear the repository.
- Support iteration and len().
- Support the ``in`` operator.

Version
-------
v0.5.2
"""

from dataclasses import dataclass, field

from SanskritAI.acquisition.models.corpus_source import CorpusSource


@dataclass
class DefaultSourceRepository:
    """
    Default in-memory repository for CorpusSource objects.
    """

    _sources: dict[str, CorpusSource] = field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def add(
        self,
        source: CorpusSource,
    ) -> CorpusSource:
        """
        Register a CorpusSource.

        Raises
        ------
        ValueError
            If the source_id is already registered.
        """

        source_id = source.source_id

        if self.exists(source_id):
            raise ValueError(
                f"Source already registered: {source_id}"
            )

        self._sources[source_id] = source

        return source

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get(
        self,
        source_id: str,
    ) -> CorpusSource | None:
        """
        Retrieve a source by source_id.

        Returns None when the source is not registered.
        """

        return self._sources.get(source_id)

    # ------------------------------------------------------------------
    # Existence
    # ------------------------------------------------------------------

    def exists(
        self,
        source_id: str,
    ) -> bool:
        """
        Return True when source_id is registered.
        """

        return source_id in self._sources

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def all(
        self,
    ) -> tuple[CorpusSource, ...]:
        """
        Return an immutable snapshot of all registered sources.

        A tuple is deliberately returned so callers cannot mutate
        the repository's internal collection.
        """

        return tuple(
            self._sources.values()
        )

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def remove(
        self,
        source_id: str,
    ) -> CorpusSource | None:
        """
        Remove and return a registered source.

        Returns None when the source does not exist.
        """

        return self._sources.pop(
            source_id,
            None,
        )

    # ------------------------------------------------------------------
    # Clear
    # ------------------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove all registered sources.
        """

        self._sources.clear()

    # ------------------------------------------------------------------
    # Protocols
    # ------------------------------------------------------------------

    def __contains__(
        self,
        source_id: str,
    ) -> bool:
        """
        Support:

            source_id in repository
        """

        return self.exists(source_id)

    def __len__(
        self,
    ) -> int:
        """
        Return the number of registered sources.
        """

        return len(self._sources)

    def __iter__(self):
        """
        Iterate over registered CorpusSource objects.
        """

        return iter(
            self._sources.values()
        )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(count={len(self)})"
        )

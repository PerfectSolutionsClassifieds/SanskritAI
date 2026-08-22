from __future__ import annotations

"""
SanskritAI
==========

Default Source Repository

Canonical in-memory repository implementation for CorpusSource.

Responsibilities
----------------

• Register CorpusSource instances.
• Prevent duplicate source identifiers.
• Retrieve sources by source_id.
• Determine whether a source exists.
• Return an immutable snapshot of registered sources.
• Remove sources.
• Clear the repository.
• Support iteration and len().
• Support the ``in`` operator.

The repository stores CorpusSource metadata only.

Version
-------
v0.5.1
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
        Registers a source.

        Parameters
        ----------
        source:
            CorpusSource to register.

        Returns
        -------
        CorpusSource
            The registered source.

        Raises
        ------
        ValueError
            If a source with the same source_id already exists.
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
        Returns a registered source by source_id.

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
        Returns True when source_id is registered.
        """

        return source_id in self._sources

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    @property
    def all(
        self,
    ) -> tuple[CorpusSource, ...]:
        """
        Returns an immutable snapshot of all registered sources.
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
        Removes and returns a registered source.

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
        Removes all registered sources.
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
        Supports:

            source_id in repository
        """

        return self.exists(
            source_id,
        )

    def __len__(
        self,
    ) -> int:
        """
        Returns the number of registered sources.
        """

        return len(
            self._sources
        )

    def __iter__(
        self,
    ):
        """
        Iterates over registered CorpusSource objects.
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

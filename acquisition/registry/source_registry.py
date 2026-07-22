
from __future__ import annotations

"""
SanskritAI
==========

Source Registry

Provides the central registry service for CorpusSource objects.

The SourceRegistry is responsible for:

    • Registering corpus sources
    • Unregistering corpus sources
    • Discovering registered sources
    • Loading manifests (future)
    • Persisting the registry (future)

The registry intentionally does NOT:

    • Download files
    • Validate files
    • Normalize metadata
    • Import corpora

Those responsibilities belong to dedicated services.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from collections.abc import Iterable
from pathlib import Path

from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_type import SourceType
from SanskritAI.acquisition.registry.source_catalog import SourceCatalog


class SourceRegistry:
    """
    Service responsible for managing the catalog of corpus sources.
    """

    def __init__(
        self,
        catalog: SourceCatalog | None = None,
    ) -> None:
        self._catalog = catalog or SourceCatalog()

    # ------------------------------------------------------------------
    # Catalog
    # ------------------------------------------------------------------

    @property
    def catalog(self) -> SourceCatalog:
        """
        Returns the underlying source catalog.
        """
        return self._catalog

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        source: CorpusSource,
    ) -> None:
        """
        Registers a corpus source.

        Raises
        ------
        ValueError
            If the source already exists.
        """
        self._catalog.add(source)

    def unregister(
        self,
        source_id: str,
    ) -> CorpusSource:
        """
        Removes a corpus source.

        Raises
        ------
        KeyError
            If the source does not exist.
        """
        return self._catalog.remove(source_id)

    def is_registered(
        self,
        source_id: str,
    ) -> bool:
        """
        Returns True if the source is registered.
        """
        return self._catalog.contains(source_id)

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
        return self._catalog.get(source_id)

    def require(
        self,
        source_id: str,
    ) -> CorpusSource:
        """
        Returns the source.

        Raises
        ------
        KeyError
            If the source is unknown.
        """
        return self._catalog.require(source_id)

    def all_sources(self) -> list[CorpusSource]:
        """
        Returns all registered sources.
        """
        return self._catalog.values()

    def sources_by_type(
        self,
        source_type: SourceType,
    ) -> list[CorpusSource]:
        """
        Returns all sources of the specified type.
        """
        return self._catalog.by_type(source_type)

    # ------------------------------------------------------------------
    # Bulk Registration
    # ------------------------------------------------------------------

    def register_many(
        self,
        sources: Iterable[CorpusSource],
    ) -> None:
        """
        Registers multiple sources.
        """
        for source in sources:
            self.register(source)

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[CorpusSource]:
        """
        Discovers all currently registered sources.

        Future versions may also discover sources from:

            • JSON manifests
            • YAML manifests
            • Python plugins
            • Remote catalogs

        Currently this simply returns the catalog contents.
        """
        return self.all_sources()

    # ------------------------------------------------------------------
    # Manifest Support
    # ------------------------------------------------------------------

    def load_manifest(
        self,
        path: str | Path,
    ) -> AcquisitionManifest:
        """
        Loads an AcquisitionManifest from disk.

        Notes
        -----
        JSON/YAML manifest loading will be implemented in a
        future commit.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError(
            "Manifest loading will be implemented "
            "in a future commit."
        )

    def save_manifest(
        self,
        manifest: AcquisitionManifest,
        path: str | Path,
    ) -> None:
        """
        Saves an AcquisitionManifest.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError(
            "Manifest serialization will be implemented "
            "in a future commit."
        )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load_registry(
        self,
        path: str | Path,
    ) -> None:
        """
        Loads a registry from persistent storage.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError(
            "Registry persistence will be implemented "
            "in a future commit."
        )

    def save_registry(
        self,
        path: str | Path,
    ) -> None:
        """
        Saves the registry.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError(
            "Registry persistence will be implemented "
            "in a future commit."
        )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def source_count(self) -> int:
        """
        Returns the number of registered sources.
        """
        return len(self._catalog)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no sources are registered.
        """
        return len(self._catalog) == 0

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._catalog)

    def __iter__(self):
        return iter(self._catalog)

    def __repr__(self) -> str:
        return (
            f"SourceRegistry("
            f"sources={len(self._catalog)})"
        )


from __future__ import annotations

"""
SanskritAI
==========

Base Discovery Provider

Defines the abstract interface implemented by every corpus
discovery provider.

Discovery providers are responsible for locating available
corpus resources from one specific source.

Examples
--------
    • LocalDirectoryProvider
    • GRETILProvider
    • CologneProvider
    • SARITProvider
    • MuktabodhaProvider
    • SanskritDocumentsProvider

Discovery providers intentionally do NOT perform:

    • downloading
    • validation
    • normalization
    • parsing
    • importing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from abc import ABC, abstractmethod
from typing import Iterable

from SanskritAI.acquisition.models.corpus_source import CorpusSource


class BaseDiscoveryProvider(ABC):
    """
    Abstract base class for all corpus discovery providers.
    """

    def __init__(
        self,
        *,
        enabled: bool = True,
    ) -> None:

        self._enabled = enabled
        self._name = self.__class__.__name__

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Human-readable provider name.
        """
        return self._name

    @property
    def enabled(self) -> bool:
        """
        Returns whether this provider participates in discovery.
        """
        return self._enabled

    @enabled.setter
    def enabled(
        self,
        value: bool,
    ) -> None:
        self._enabled = bool(value)

    # ------------------------------------------------------------------
    # Abstract Discovery API
    # ------------------------------------------------------------------

    @abstractmethod
    def discover(self) -> Iterable[CorpusSource]:
        """
        Discover available corpus resources.

        Returns
        -------
        Iterable[CorpusSource]
            Zero or more discovered corpus sources.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Optional Hooks
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Optional initialization hook.

        Subclasses may override this method to establish
        connections, prepare caches, authenticate with remote
        services, or perform other setup tasks.
        """
        return None

    def shutdown(self) -> None:
        """
        Optional cleanup hook.

        Called when the provider is no longer needed.
        """
        return None

    def refresh(self) -> Iterable[CorpusSource]:
        """
        Refresh discovery results.

        The default implementation simply invokes discover().
        """
        return self.discover()

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Indicates whether the provider is currently available.

        Subclasses may override this to perform health checks,
        verify connectivity, or inspect local resources.
        """
        return self.enabled

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(enabled={self.enabled})"
        )

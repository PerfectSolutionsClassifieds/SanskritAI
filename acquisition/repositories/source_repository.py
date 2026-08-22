from __future__ import annotations

"""
SanskritAI
==========

Source Repository

Defines the repository abstraction for canonical corpus sources.

The repository is responsible only for managing CorpusSource
metadata. Acquisition, downloading, parsing, validation, and
normalization belong to higher acquisition layers.

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from typing import Iterable

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.core.mixins.displayable import Displayable


class SourceRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for canonical CorpusSource objects.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Repository for canonical corpus-source metadata."
        )

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> CorpusSource | None:
        """
        Returns a source by identifier.

        Returns None when the source does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Returns True when a source exists.
        """
        raise NotImplementedError

    @abstractmethod
    def all(
        self,
    ) -> Iterable[CorpusSource]:
        """
        Returns all registered sources.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Mutation
    # ---------------------------------------------------------

    @abstractmethod
    def add(
        self,
        source: CorpusSource,
    ) -> CorpusSource:
        """
        Registers a new source.

        Implementations should reject duplicate identifiers.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        identifier: str,
    ) -> CorpusSource | None:
        """
        Removes and returns a source.

        Returns None when the source does not exist.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Collection
    # ---------------------------------------------------------

    def count(self) -> int:
        """
        Returns the number of registered sources.
        """
        return sum(
            1
            for _ in self.all()
        )

    def is_empty(self) -> bool:
        """
        Returns True when no sources are registered.
        """
        return self.count() == 0

    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.count()

    def __contains__(
        self,
        identifier: str,
    ) -> bool:
        return self.exists(identifier)

    def __str__(self) -> str:
        return self.display_text

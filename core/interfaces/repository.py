from __future__ import annotations

"""
SanskritAI
==========

Repository Interface

Defines the canonical contract for repositories that manage
domain objects.

A repository abstracts the lifecycle of domain objects without
prescribing how they are stored. Implementations may use
in-memory collections, databases, files, remote services, or
other persistence mechanisms.

Typical Implementations
-----------------------

- CorpusRegistry
- LexiconRegistry
- GrammarRegistry
- MongoRepository
- SQLRepository

Version
-------
v0.3.0
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Generic

from SanskritAI.core.typing import (
    T,
    TIdentifier,
)


class Repository(
    Generic[TIdentifier, T],
    ABC,
):
    """
    Generic repository contract.
    """

    # ---------------------------------------------------------
    # CRUD Operations
    # ---------------------------------------------------------

    @abstractmethod
    def add(
        self,
        obj: T,
    ) -> None:
        """
        Store an object.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def remove(
        self,
        identifier: TIdentifier,
    ) -> None:
        """
        Remove an object by its identifier.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def get(
        self,
        identifier: TIdentifier,
    ) -> T | None:
        """
        Retrieve an object by its identifier.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def exists(
        self,
        identifier: TIdentifier,
    ) -> bool:
        """
        Returns True if the identifier exists.
        """
        ...

    # ---------------------------------------------------------
    # Collection Operations
    # ---------------------------------------------------------

    @abstractmethod
    def all(
        self,
    ) -> Iterable[T]:
        """
        Return all stored objects.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove all objects.
        """
        ...

    # ---------------------------------------------------------
    # Convenience Methods
    # ---------------------------------------------------------

    def __contains__(
        self,
        identifier: TIdentifier,
    ) -> bool:
        """
        Support: identifier in repository
        """

        return self.exists(identifier)

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[T]:
        """
        Iterate over stored objects.
        """

        return iter(self.all())

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Number of stored objects.
        """

        return sum(1 for _ in self.all())

from __future__ import annotations

"""
SanskritAI
==========

Base Registry

Generic in-memory repository implementation.

This class provides the reusable storage implementation for
registries throughout SanskritAI while remaining completely
independent of domain-specific models.

Version
-------
v0.3.0
"""

from collections.abc import Iterable, Iterator
from typing import Generic

from SanskritAI.core.interfaces.identifiable import (
    Identifiable,
)
from SanskritAI.core.interfaces.repository import (
    Repository,
)
from SanskritAI.core.typing import (
    T,
    TIdentifier,
)


class BaseRegistry(
    Repository[TIdentifier, T],
    Generic[TIdentifier, T],
):
    """
    Generic in-memory registry.

    Parameters
    ----------
    TIdentifier
        Identifier type.

    T
        Stored object type. The object must expose an ``id``
        property compatible with ``TIdentifier``.
    """

    def __init__(self) -> None:
        self._items: dict[TIdentifier, T] = {}

    # ---------------------------------------------------------
    # CRUD Operations
    # ---------------------------------------------------------

    def add(
        self,
        obj: T,
    ) -> None:
        """
        Register an object.
        """

        identifier = getattr(obj, "id")

        self._items[identifier] = obj

    # ---------------------------------------------------------

    def remove(
        self,
        identifier: TIdentifier,
    ) -> None:
        """
        Remove an object.
        """

        self._items.pop(identifier, None)

    # ---------------------------------------------------------

    def get(
        self,
        identifier: TIdentifier,
    ) -> T | None:
        """
        Retrieve an object.
        """

        return self._items.get(identifier)

    # ---------------------------------------------------------

    def exists(
        self,
        identifier: TIdentifier,
    ) -> bool:
        """
        Returns True if an object exists.
        """

        return identifier in self._items

    # ---------------------------------------------------------

    def all(
        self,
    ) -> Iterable[T]:
        """
        Return all registered objects.
        """

        return self._items.values()

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove all objects.
        """

        self._items.clear()

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def identifiers(
        self,
    ) -> Iterable[TIdentifier]:
        """
        Return all identifiers.
        """

        return self._items.keys()

    # ---------------------------------------------------------

    def values(
        self,
    ) -> Iterable[T]:
        """
        Alias for ``all()``.
        """

        return self._items.values()

    # ---------------------------------------------------------

    def items(
        self,
    ) -> Iterable[tuple[TIdentifier, T]]:
        """
        Iterate over identifier-object pairs.
        """

        return self._items.items()

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[T]:

        return iter(self._items.values())

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._items)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(count={len(self)})"
        )

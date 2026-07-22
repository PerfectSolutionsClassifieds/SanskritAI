from __future__ import annotations

"""
SanskritAI
==========

Registry

Defines the canonical root abstraction for all SanskritAI
registries.

A Registry is a generic container responsible for registering,
organizing, discovering, and retrieving architectural
components.

Concrete subclasses determine the storage strategy, ordering,
typing constraints, and lookup semantics.

Typical registry contents include:

- Builders
- Validators
- Parsers
- Tokenizers
- Dictionaries
- Corpora
- Plugins
- AI Models
- Processing Engines

Architecture
------------

Registry
    ├── MutableRegistry
    ├── ImmutableRegistry
    ├── TypedRegistry
    ├── OrderedRegistry
    └── HierarchicalRegistry

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from typing import Generic, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Registry(ABC, Generic[K, V]):
    """
    Root abstraction for all SanskritAI registries.
    """

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @abstractmethod
    def register(
        self,
        key: K,
        value: V,
    ) -> None:
        """
        Registers a value under the supplied key.
        """
        raise NotImplementedError

    @abstractmethod
    def unregister(
        self,
        key: K,
    ) -> V | None:
        """
        Removes the value associated with the supplied key.

        Returns
        -------
        V | None
            Removed value if present.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def contains(
        self,
        key: K,
    ) -> bool:
        """
        Returns True if the key exists.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        key: K,
    ) -> V | None:
        """
        Returns the registered value.

        Returns
        -------
        V | None
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    @abstractmethod
    def keys(self) -> Iterator[K]:
        """
        Returns an iterator over registry keys.
        """
        raise NotImplementedError

    @abstractmethod
    def values(self) -> Iterator[V]:
        """
        Returns an iterator over registered values.
        """
        raise NotImplementedError

    @abstractmethod
    def items(self) -> Iterator[tuple[K, V]]:
        """
        Returns an iterator over registry entries.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    @abstractmethod
    def clear(self) -> None:
        """
        Removes all registered entries.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def size(self) -> int:
        """
        Number of registered entries.
        """
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the registry contains no entries.
        """
        return self.size == 0

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: object) -> bool:
        return self.contains(key)  # type: ignore[arg-type]

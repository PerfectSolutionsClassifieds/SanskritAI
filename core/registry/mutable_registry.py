from __future__ import annotations

"""
SanskritAI
==========

Mutable Registry

Concrete implementation of the Registry abstraction using an
in-memory mutable mapping.

MutableRegistry serves as the reference implementation for all
other registry types.

Architecture
------------

Registry
    │
    ▼
MutableRegistry
    │
    ├── TypedRegistry
    ├── OrderedRegistry
    ├── HierarchicalRegistry
    └── ImmutableRegistry

Version
-------
v0.6.0
"""

from typing import Dict, Iterator, Generic, TypeVar

from SanskritAI.core.registry.registry import Registry
from SanskritAI.core.registry.registry_entry import RegistryEntry
from SanskritAI.core.registry.registry_exception import RegistryException
from SanskritAI.core.registry.registry_key import RegistryKey


K = TypeVar("K", bound=RegistryKey)
V = TypeVar("V")


class MutableRegistry(Registry[K, V], Generic[K, V]):
    """
    Default mutable registry implementation.
    """

    def __init__(self) -> None:
        self._entries: Dict[K, RegistryEntry] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        key: K,
        value: V,
    ) -> None:
        if key in self._entries:
            raise RegistryException(
                f"Registry key '{key}' is already registered.",
                key=key,
                value=value,
            )

        self._entries[key] = RegistryEntry(
            key=key,
            value=value,
        )

    def unregister(
        self,
        key: K,
    ) -> V | None:
        entry = self._entries.pop(key, None)

        if entry is None:
            return None

        return entry.value

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def contains(
        self,
        key: K,
    ) -> bool:
        return key in self._entries

    def get(
        self,
        key: K,
    ) -> V | None:
        entry = self._entries.get(key)

        if entry is None:
            return None

        return entry.value

    def get_entry(
        self,
        key: K,
    ) -> RegistryEntry | None:
        """
        Returns the complete registry entry.
        """
        return self._entries.get(key)

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def keys(self) -> Iterator[K]:
        return iter(self._entries.keys())

    def values(self) -> Iterator[V]:
        for entry in self._entries.values():
            yield entry.value

    def items(self):
        for key, entry in self._entries.items():
            yield key, entry.value

    def entries(self) -> Iterator[RegistryEntry]:
        """
        Returns all registry entries.
        """
        return iter(self._entries.values())

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear(self) -> None:
        self._entries.clear()

    @property
    def size(self) -> int:
        return len(self._entries)

from __future__ import annotations

"""
SanskritAI
==========

Ordered Registry

Defines a typed registry that preserves insertion order.

OrderedRegistry extends TypedRegistry by guaranteeing
deterministic iteration over registered entries.

This registry serves as the foundation for hierarchical
registries, corpus navigation, plugin loading, and ordered
processing pipelines.

Typical usages include:

- Plugin Registry
- Corpus Registry
- Processing Pipeline Registry
- Dictionary Registry

Architecture
------------

Registry
      │
      ▼
MutableRegistry
      │
      ▼
TypedRegistry
      │
      ▼
OrderedRegistry

Version
-------
v0.6.0
"""

from collections import OrderedDict
from typing import Iterator, Generic, TypeVar

from SanskritAI.core.registry.registry_entry import RegistryEntry
from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.registry.typed_registry import TypedRegistry

K = TypeVar("K", bound=RegistryKey)
V = TypeVar("V")


class OrderedRegistry(TypedRegistry[K, V], Generic[K, V]):
    """
    Registry preserving insertion order.
    """

    def __init__(
        self,
        value_type: type[V],
    ) -> None:
        super().__init__(value_type)

        # Replace the default storage with an ordered mapping.
        self._entries: OrderedDict[K, RegistryEntry] = OrderedDict()

    @property
    def is_ordered(self) -> bool:
        """
        Indicates that this registry preserves insertion order.
        """
        return True

    def first(self) -> RegistryEntry | None:
        """
        Returns the first registered entry.
        """
        if not self._entries:
            return None

        return next(iter(self._entries.values()))

    def last(self) -> RegistryEntry | None:
        """
        Returns the last registered entry.
        """
        if not self._entries:
            return None

        return next(reversed(self._entries.values()))

    def entries(self) -> Iterator[RegistryEntry]:
        """
        Returns registry entries in insertion order.
        """
        yield from self._entries.values()

    def reversed_entries(self) -> Iterator[RegistryEntry]:
        """
        Returns registry entries in reverse insertion order.
        """
        yield from reversed(self._entries.values())

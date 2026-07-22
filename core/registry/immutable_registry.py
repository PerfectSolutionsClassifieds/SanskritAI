from __future__ import annotations

"""
SanskritAI
==========

Immutable Registry

Defines a read-only registry whose contents cannot be modified
after construction.

ImmutableRegistry is intended for production registries,
canonical resources, loaded dictionaries, parser registries,
and other stable infrastructure components.

Architecture
------------

Registry
      │
      ▼
TypedRegistry
      │
      ▼
ImmutableRegistry

Version
-------
v0.6.0
"""

from typing import Generic, Iterable, TypeVar

from SanskritAI.core.registry.registry_entry import RegistryEntry
from SanskritAI.core.registry.registry_exception import RegistryException
from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.registry.typed_registry import TypedRegistry

K = TypeVar("K", bound=RegistryKey)
V = TypeVar("V")


class ImmutableRegistry(TypedRegistry[K, V], Generic[K, V]):
    """
    Read-only registry.
    """

    def __init__(
        self,
        value_type: type[V],
        entries: Iterable[RegistryEntry] | None = None,
    ) -> None:
        super().__init__(value_type)

        if entries is not None:
            for entry in entries:
                super().register(
                    entry.key,
                    entry.value,
                )

    # ---------------------------------------------------------
    # Mutation operations
    # ---------------------------------------------------------

    def register(
        self,
        key: K,
        value: V,
    ) -> None:
        raise RegistryException(
            "ImmutableRegistry does not permit registration.",
            key=key,
            value=value,
        )

    def unregister(
        self,
        key: K,
    ) -> V | None:
        raise RegistryException(
            "ImmutableRegistry does not permit unregistration.",
            key=key,
        )

    def clear(self) -> None:
        raise RegistryException(
            "ImmutableRegistry cannot be cleared."
        )

    # ---------------------------------------------------------
    # Characteristics
    # ---------------------------------------------------------

    @property
    def is_mutable(self) -> bool:
        """
        Indicates whether the registry supports mutation.
        """
        return False

    @property
    def is_immutable(self) -> bool:
        """
        Indicates that this registry is immutable.
        """
        return True

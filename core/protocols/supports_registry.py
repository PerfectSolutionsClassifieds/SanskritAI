from __future__ import annotations

"""
SanskritAI
==========

SupportsRegistry Protocol

Defines the structural protocol for registry-like components.

Unlike the Registry classes themselves, this protocol specifies
only the minimal structural interface required for registration
and retrieval.

Typical implementations include:

- Registry
- TypedRegistry
- OrderedRegistry
- HierarchicalRegistry
- ImmutableRegistry (read-only registration not supported)
- Plugin Registry
- Service Registry
- Configuration Registry

Architecture
------------

Protocol
      │
      ▼
SupportsRegistry

Version
-------
v0.6.0
"""

from typing import Generic
from typing import Iterator
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol

K = TypeVar("K")
V = TypeVar("V")


@runtime_checkable
class SupportsRegistry(Protocol, Generic[K, V]):
    """
    Structural protocol for registry-like components.
    """

    def register(
        self,
        key: K,
        value: V,
    ) -> None:
        """
        Registers a value under the supplied key.
        """
        ...

    def unregister(
        self,
        key: K,
    ) -> V | None:
        """
        Removes and returns the value associated with the key.

        Returns
        -------
        V | None
            The removed value, if present.
        """
        ...

    def lookup(
        self,
        key: K,
        default: V | None = None,
    ) -> V | None:
        """
        Retrieves the value associated with the supplied key.
        """
        ...

    def __contains__(
        self,
        key: object,
    ) -> bool:
        """
        Returns True if the supplied key exists.
        """
        ...

    def __len__(self) -> int:
        """
        Returns the number of registered entries.
        """
        ...

    def __iter__(self) -> Iterator[K]:
        """
        Iterates over registered keys.
        """
        ...

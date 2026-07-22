from __future__ import annotations

"""
SanskritAI
==========

SupportsLookup Protocol

Defines the structural protocol for components that support
key-based lookup operations.

Unlike semantic Contracts, this protocol specifies only the
required structural interface and enables structural typing
(PEP 544).

Typical implementations include:

- Registry
- Dictionary
- Corpus
- Knowledge Repository
- Configuration Store
- Cache
- Plugin Registry

Architecture
------------

Protocol
      │
      ▼
SupportsLookup

Version
-------
v0.6.0
"""

from typing import Any
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol

K = TypeVar("K")
V = TypeVar("V")


@runtime_checkable
class SupportsLookup(Protocol[K, V]):
    """
    Structural protocol for key-based lookup.
    """

    def lookup(
        self,
        key: K,
        default: V | None = None,
    ) -> V | None:
        """
        Returns the value associated with the supplied key.

        Parameters
        ----------
        key:
            Lookup key.

        default:
            Value returned if the key is not found.

        Returns
        -------
        V | None
            The associated value, or the supplied default.
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

    def __getitem__(
        self,
        key: K,
    ) -> V:
        """
        Retrieves the value associated with the supplied key.

        Raises
        ------
        KeyError
            If the key does not exist.
        """
        ...

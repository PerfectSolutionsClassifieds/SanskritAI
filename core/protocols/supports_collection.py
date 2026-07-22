from __future__ import annotations

"""
SanskritAI
==========

SupportsCollection Protocol

Defines the structural protocol for collection-like objects.

A collection exposes iterable semantics together with
membership testing and size information.

Unlike semantic Contracts, this protocol specifies only the
required structural interface and enables structural typing
(PEP 544).

Typical implementations include:

- Registry
- SearchResult
- DiagnosticCollection
- TokenStream
- Corpus
- Lexicon
- Knowledge Repository

Architecture
------------

Protocol
      │
      ▼
SupportsIteration
      │
      ▼
SupportsCollection

Version
-------
v0.6.0
"""

from collections.abc import Sized, Container
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol
from SanskritAI.core.protocols.supports_iteration import SupportsIteration

T = TypeVar("T")


@runtime_checkable
class SupportsCollection(
    Protocol,
    SupportsIteration[T],
    Sized,
    Container[T],
):
    """
    Structural protocol for collection-like objects.
    """

    def __len__(self) -> int:
        """
        Returns the number of contained elements.
        """
        ...

    def __contains__(self, item: object) -> bool:
        """
        Returns True if the supplied item exists within the
        collection.
        """
        ...

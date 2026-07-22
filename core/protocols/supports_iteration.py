from __future__ import annotations

"""
SanskritAI
==========

SupportsIteration Protocol

Defines the structural protocol for iterable components.

This protocol identifies objects that expose a standard Python
iteration interface. It serves as the foundational protocol for
many higher-level SanskritAI components such as registries,
token streams, search results, diagnostic collections, corpora,
and lexical repositories.

Unlike semantic Contracts, this protocol specifies only the
required structural interface and enables structural typing
(PEP 544).

Typical implementations include:

- Registry
- TokenStream
- SearchResult
- DiagnosticCollection
- Corpus
- Lexicon
- Knowledge Repository

Architecture
------------

typing.Iterable
        │
        ▼
Protocol
        │
        ▼
SupportsIteration

Version
-------
v0.6.0
"""

from collections.abc import Iterable, Iterator
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol

T = TypeVar("T")


@runtime_checkable
class SupportsIteration(Protocol, Iterable[T]):
    """
    Structural protocol for iterable components.
    """

    def __iter__(self) -> Iterator[T]:
        """
        Returns an iterator over the contained elements.
        """
        ...

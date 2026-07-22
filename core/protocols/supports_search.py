from __future__ import annotations

"""
SanskritAI
==========

SupportsSearch Protocol

Defines the structural protocol for searchable components.

This protocol specifies the minimal interface required for
objects capable of executing search operations.

Unlike semantic Contracts, this protocol specifies only the
required structural interface and enables structural typing
(PEP 544).

Typical implementations include:

- Corpus
- Lexicon
- Dictionary
- Amarakośa
- Knowledge Repository
- Search Engine
- Vector Database Adapter

Architecture
------------

Protocol
      │
      ▼
SupportsSearch

Version
-------
v0.6.0
"""

from typing import Generic
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol

Q = TypeVar("Q")  # Query type
R = TypeVar("R")  # Result type


@runtime_checkable
class SupportsSearch(Protocol, Generic[Q, R]):
    """
    Structural protocol for searchable components.
    """

    def search(
        self,
        query: Q,
    ) -> R:
        """
        Executes a search.

        Parameters
        ----------
        query:
            Search request.

        Returns
        -------
        R
            Search result.
        """
        ...

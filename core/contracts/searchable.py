from __future__ import annotations

"""
SanskritAI
==========

Searchable Contract

Defines the contract for components capable of searching
their internal contents using a query.

Typical implementations include:

- Corpus
- Dictionary
- Amarakosha
- Knowledge Repository
- Registry
- Index
- Search Engine

Architecture
------------

Contract
      │
      ▼
Searchable

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import Any, Iterable

from SanskritAI.core.contracts.contract import Contract


class Searchable(Contract):
    """
    Contract for searchable components.
    """

    @abstractmethod
    def search(
        self,
        query: Any,
    ) -> Iterable[Any]:
        """
        Searches the component using the supplied query.

        Parameters
        ----------
        query:
            Search query.

        Returns
        -------
        Iterable[Any]
            Zero or more matching results.
        """
        raise NotImplementedError

    def contains(
        self,
        query: Any,
    ) -> bool:
        """
        Returns True if at least one matching result exists.

        This default implementation is derived from ``search()``
        and may be overridden by subclasses for efficiency.
        """
        return any(True for _ in self.search(query))

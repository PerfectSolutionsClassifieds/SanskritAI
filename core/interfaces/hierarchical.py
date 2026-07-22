from __future__ import annotations

"""
SanskritAI
==========

Hierarchical Interface

Defines the contract for objects participating in a tree
structure.

This interface is intentionally generic and reusable across
Corpus, Grammar, Knowledge Graph, and future modules.

Version
-------
v0.3.0
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic

from SanskritAI.core.typing import TChild


class Hierarchical(
    Generic[TChild],
    ABC,
):
    """
    Contract for hierarchical objects.
    """

    # ---------------------------------------------------------

    @property
    @abstractmethod
    def children(
        self,
    ) -> Iterable[TChild]:
        """
        Returns the child objects.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def add_child(
        self,
        child: TChild,
    ) -> None:
        """
        Add a child object.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def remove_child(
        self,
        child: TChild,
    ) -> None:
        """
        Remove a child object.
        """
        ...

    # ---------------------------------------------------------

    @property
    def child_count(
        self,
    ) -> int:
        """
        Number of child objects.
        """

        return len(tuple(self.children))

    # ---------------------------------------------------------

    @property
    def is_leaf(
        self,
    ) -> bool:
        """
        True if this node has no children.
        """

        return self.child_count == 0

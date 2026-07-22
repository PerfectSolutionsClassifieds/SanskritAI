from __future__ import annotations

"""
SanskritAI
==========

Container Node

Abstract base class for canonical corpus nodes that contain
child nodes.

This class delegates child storage and management to
NodeCollection, providing a clean separation between node
behavior and collection behavior.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line

Token intentionally does NOT inherit from ContainerNode.

Version
-------
v0.3.0
"""

from abc import ABC
from collections.abc import Iterable, Iterator
from typing import Generic

from SanskritAI.core.collections.node_collection import (
    NodeCollection,
)
from SanskritAI.core.interfaces.hierarchical import (
    Hierarchical,
)
from SanskritAI.core.typing import (
    TChild,
    TIdentifier,
    TMetadata,
)

from SanskritAI.corpus.models.base_node import BaseNode


class ContainerNode(
    BaseNode[TIdentifier, TMetadata],
    Hierarchical[TChild],
    Generic[TIdentifier, TMetadata, TChild],
    ABC,
):
    """
    Abstract base class for nodes that own child nodes.
    """

    # ---------------------------------------------------------

    def __init__(
        self,
        identifier: TIdentifier,
        metadata: TMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

        self._children = NodeCollection[TChild]()

    # ---------------------------------------------------------
    # Hierarchical Interface
    # ---------------------------------------------------------

    @property
    def children(
        self,
    ) -> NodeCollection[TChild]:
        """
        Child node collection.
        """

        return self._children

    # ---------------------------------------------------------

    def add_child(
        self,
        child: TChild,
    ) -> None:
        """
        Add a child node.
        """

        self._children.add(child)

    # ---------------------------------------------------------

    def remove_child(
        self,
        child: TChild,
    ) -> None:
        """
        Remove a child node.
        """

        self._children.remove(child)

    # ---------------------------------------------------------

    def extend(
        self,
        children: Iterable[TChild],
    ) -> None:
        """
        Add multiple child nodes.
        """

        self._children.extend(children)

    # ---------------------------------------------------------

    def clear_children(
        self,
    ) -> None:
        """
        Remove all child nodes.
        """

        self._children.clear()

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def child_count(
        self,
    ) -> int:
        """
        Number of child nodes.
        """

        return len(self._children)

    # ---------------------------------------------------------

    @property
    def is_leaf(
        self,
    ) -> bool:
        """
        True if the node has no children.
        """

        return len(self._children) == 0

    # ---------------------------------------------------------

    @property
    def first_child(
        self,
    ) -> TChild | None:
        """
        First child node.
        """

        return self._children.first()

    # ---------------------------------------------------------

    @property
    def last_child(
        self,
    ) -> TChild | None:
        """
        Last child node.
        """

        return self._children.last()

    # ---------------------------------------------------------
    # Python Protocols
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[TChild]:

        return iter(self._children)

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> TChild:

        return self._children[index]

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._children)

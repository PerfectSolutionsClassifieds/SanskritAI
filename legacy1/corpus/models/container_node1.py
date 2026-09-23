from __future__ import annotations

"""
SanskritAI
==========

Container Node

Defines the abstract base class for canonical corpus nodes
that may contain child nodes.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line

Token is intentionally NOT a ContainerNode.

Version
-------
v0.3.0
"""

from abc import ABC
from collections.abc import Iterable, Iterator
from typing import Generic

from SanskritAI.core.interfaces.hierarchical import (
    Hierarchical,
)
from SanskritAI.core.typing import (
    TChild,
    TIdentifier,
    TMetadata,
)

from SanskritAI.corpus.models.base_node import (
    BaseNode,
)


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

        self._children: list[TChild] = []

    # ---------------------------------------------------------
    # Hierarchical interface
    # ---------------------------------------------------------

    @property
    def children(
        self,
    ) -> Iterable[TChild]:
        """
        Return the child nodes.
        """

        return tuple(self._children)

    # ---------------------------------------------------------

    def add_child(
        self,
        child: TChild,
    ) -> None:
        """
        Add a child node.
        """

        self._children.append(child)

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
    # Convenience
    # ---------------------------------------------------------

    def clear_children(
        self,
    ) -> None:
        """
        Remove all child nodes.
        """

        self._children.clear()

    # ---------------------------------------------------------

    def extend(
        self,
        children: Iterable[TChild],
    ) -> None:
        """
        Append multiple child nodes.
        """

        self._children.extend(children)

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
        True if no child nodes exist.
        """

        return not self._children

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[TChild]:
        """
        Iterate over child nodes.
        """

        return iter(self._children)

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Number of child nodes.
        """

        return len(self._children)

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> TChild:
        """
        Random access to child nodes.
        """

        return self._children[index]

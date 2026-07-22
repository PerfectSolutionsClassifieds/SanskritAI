from __future__ import annotations

"""
SanskritAI
==========

Child Node Builder

Intermediate generic builder for canonical nodes that own a
homogeneous collection of child nodes.

This class extends NodeBuilder with reusable helper methods for
adding collections of child objects while keeping concrete builders
focused on domain-specific operations.

Derived Builders
----------------
* VerseBuilder
* ParagraphBuilder
* LineBuilder

Version
-------
v0.1.0
"""

from typing import Callable, Generic, Iterable, Self, TypeVar

from SanskritAI.corpus.builders.node_builder import (
    NodeBuilder,
)

TNode = TypeVar("TNode")
TMetadata = TypeVar("TMetadata")
TChild = TypeVar("TChild")


class ChildNodeBuilder(
    NodeBuilder[TNode, TMetadata],
    Generic[TNode, TMetadata, TChild],
):
    """
    Generic builder for nodes containing homogeneous child collections.
    """

    # ---------------------------------------------------------
    # Generic child helpers
    # ---------------------------------------------------------

    def _add_child(
        self,
        child: TChild,
        add_method: Callable[[TChild], None],
    ) -> Self:
        """
        Add a single child using the supplied model method.
        """

        add_method(child)
        return self

    # ---------------------------------------------------------

    def _add_children(
        self,
        children: Iterable[TChild],
        add_method: Callable[[TChild], None],
    ) -> Self:
        """
        Add multiple children using the supplied model method.
        """

        for child in children:
            add_method(child)

        return self

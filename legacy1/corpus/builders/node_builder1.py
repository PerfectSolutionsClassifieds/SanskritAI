from __future__ import annotations

"""
SanskritAI
==========

Node Builder

Intermediate generic builder for all canonical corpus nodes.

This class extends BaseBuilder by providing common operations for
objects derived from BaseNode.

Responsibilities
----------------
* Metadata assignment
* Common metadata setters
* Generic validation helpers

Derived Builders
----------------
* CorpusBuilder
* DocumentBuilder
* SectionBuilder
* VerseBuilder
* ParagraphBuilder
* LineBuilder
* TokenBuilder

Version
-------
v0.1.0
"""

from typing import Generic, TypeVar

from SanskritAI.corpus.builders.base_builder import (
    BaseBuilder,
)

TNode = TypeVar("TNode")

TMetadata = TypeVar("TMetadata")


class NodeBuilder(
    BaseBuilder[TNode],
    Generic[TNode, TMetadata],
):
    """
    Generic builder for BaseNode-derived objects.
    """

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def with_metadata(
        self,
        metadata: TMetadata,
    ) -> "NodeBuilder[TNode, TMetadata]":

        self._instance.metadata = metadata

        return self

    # ---------------------------------------------------------

    def with_title(
        self,
        title: str,
    ) -> "NodeBuilder[TNode, TMetadata]":

        self._instance.metadata.title = title

        return self

    # ---------------------------------------------------------

    def with_description(
        self,
        description: str,
    ) -> "NodeBuilder[TNode, TMetadata]":

        self._instance.metadata.description = description

        return self

    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Generic node validation.
        """

        metadata = self._instance.metadata

        if hasattr(metadata, "title"):

            if not metadata.title.strip():

                raise ValueError(
                    "Node title cannot be empty."
                )

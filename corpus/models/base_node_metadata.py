from __future__ import annotations

"""
SanskritAI
==========

Base Node Metadata

Shared metadata for every canonical hierarchical node.

Purpose
-------
Provides the common identification and hierarchy fields used by
CorpusMetadata, DocumentMetadata, SectionMetadata, VerseMetadata,
ParagraphMetadata, LineMetadata and TokenMetadata.

This class intentionally does NOT contain descriptive metadata
(classification, provenance, keywords, notes, etc.), which are
provided by BaseMetadata.

Version
-------
v0.1.0
"""

from dataclasses import dataclass

from SanskritAI.corpus.models.base_metadata import (
    BaseMetadata,
)


@dataclass(slots=True)
class BaseNodeMetadata(BaseMetadata):
    """
    Base metadata shared by all canonical corpus nodes.
    """

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    title: str = ""

    canonical_title: str = ""

    short_title: str = ""

    identifier: str = ""

    # ---------------------------------------------------------
    # Hierarchy
    # ---------------------------------------------------------

    sequence_number: int | None = None

    hierarchy_level: int = 0

    parent_identifier: str = ""

    node_type: str = ""

    # ---------------------------------------------------------

    @property
    def has_identifier(self) -> bool:
        """
        Returns True if this node has a canonical identifier.
        """
        return bool(self.identifier)

    # ---------------------------------------------------------

    @property
    def is_root(self) -> bool:
        """
        Returns True if this node has no parent.
        """
        return self.parent_identifier == ""

    # ---------------------------------------------------------

    def hierarchy_dict(self) -> dict:
        """
        Serialize hierarchy-specific metadata.
        """

        return {

            "title":
                self.title,

            "canonical_title":
                self.canonical_title,

            "short_title":
                self.short_title,

            "identifier":
                self.identifier,

            "sequence_number":
                self.sequence_number,

            "hierarchy_level":
                self.hierarchy_level,

            "parent_identifier":
                self.parent_identifier,

            "node_type":
                self.node_type,

        }

    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize complete metadata.
        """

        data = self.metadata_dict()

        data.update(

            self.hierarchy_dict()

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}("

            f"title={self.title!r}, "

            f"identifier={self.identifier!r}, "

            f"level={self.hierarchy_level})"

        )

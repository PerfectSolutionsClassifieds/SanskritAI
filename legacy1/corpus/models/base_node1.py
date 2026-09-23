from __future__ import annotations

"""
SanskritAI
==========

Base Node

Abstract generic base class for all canonical corpus nodes.

Purpose
-------
Provides the common identity, metadata, parent relationship and
serialization contract shared by all corpus entities.

Derived Classes
---------------
* Document
* Section
* Verse
* Paragraph
* Line
* Token

Version
-------
v0.3.0
"""

from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from SanskritAI.common.identifiers.base_identifier import (
    BaseIdentifier,
)

from SanskritAI.corpus.models.base_metadata import (
    BaseMetadata,
)

# ---------------------------------------------------------------------
# Generic Parameters
# ---------------------------------------------------------------------

TIdentifier = TypeVar(
    "TIdentifier",
    bound=BaseIdentifier,
)

TMetadata = TypeVar(
    "TMetadata",
    bound=BaseMetadata,
)


@dataclass(slots=True)
class BaseNode(
    Generic[TIdentifier, TMetadata],
    ABC,
):
    """
    Generic base class for all canonical corpus nodes.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    id: TIdentifier

    metadata: TMetadata

    parent: "BaseNode[Any, Any] | None" = None

    # ---------------------------------------------------------
    # Parent Relationship Helpers
    # ---------------------------------------------------------

    def _attach_parent(
        self,
        child: "BaseNode[Any, Any]",
    ) -> None:
        """
        Attach a child node.
        """

        child.parent = self

    # ---------------------------------------------------------

    def _detach_parent(
        self,
        child: "BaseNode[Any, Any]",
    ) -> None:
        """
        Detach a child node.
        """

        if child.parent is self:
            child.parent = None

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def is_root(self) -> bool:
        """
        Returns True if this node has no parent.
        """

        return self.parent is None

    # ---------------------------------------------------------

    @property
    def has_parent(self) -> bool:
        """
        Returns True if this node has a parent.
        """

        return self.parent is not None

    # ---------------------------------------------------------

    @property
    def title(self) -> str:
        """
        Convenience accessor for node title.
        """

        return getattr(
            self.metadata,
            "title",
            "",
        )

    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        """
        Convenience accessor for canonical identifier.
        """

        return getattr(
            self.metadata,
            "identifier",
            "",
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the common portion of a node.

        Concrete subclasses should extend this implementation.
        """

        return {

            "id": str(self.id),

            "metadata": self.metadata.to_dict(),

        }

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}("

            f"id={self.id}, "

            f"title={self.title!r})"

        )

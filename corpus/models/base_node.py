from __future__ import annotations

"""
SanskritAI
==========

Base Node

Defines the abstract foundation for every canonical corpus node.

All structural nodes derive from BaseNode.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token

The class is intentionally lightweight and independent of
serialization or storage concerns.

Version
-------
v0.3.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.interfaces.identifiable import (
    Identifiable,
)
from SanskritAI.core.typing import (
    TIdentifier,
    TMetadata,
)


class BaseNode(
    Identifiable[TIdentifier],
    Generic[TIdentifier, TMetadata],
    ABC,
):
    """
    Abstract base class for all canonical corpus nodes.
    """

    # ---------------------------------------------------------

    def __init__(
        self,
        identifier: TIdentifier,
        metadata: TMetadata,
    ) -> None:

        self._id = identifier
        self.metadata = metadata

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def id(
        self,
    ) -> TIdentifier:
        """
        Unique identifier.
        """

        return self._id

    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> TIdentifier:
        """
        Alias for ``id``.
        """

        return self._id

    # ---------------------------------------------------------

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(other, BaseNode):
            return NotImplemented

        return (
            self.id == other.id
            and type(self) is type(other)
        )

    # ---------------------------------------------------------

    def __hash__(
        self,
    ) -> int:

        return hash(
            (
                type(self),
                self.id,
            )
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(id={self.id!r})"
        )

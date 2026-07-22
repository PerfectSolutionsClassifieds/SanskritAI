from __future__ import annotations

"""
SanskritAI
==========

Line

Canonical line within a Paragraph.

A Line groups one or more Token objects.

A Line may represent:

    • a metrical pāda
    • a printed line
    • a wrapped display line
    • a prose line

Version
-------
v0.1.0
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator

from SanskritAI.common.identifiers.line_id import (
    LineId,
)

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.corpus.models.line_metadata import (
    LineMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.token import Token


@dataclass(slots=True)
class Line(
    ContainerNode[
        LineId,
        LineMetadata,
    ]
):
    """
    Canonical Line node.
    """

    id: LineId

    metadata: LineMetadata = field(
        default_factory=LineMetadata
    )

    tokens: list["Token"] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Token Management
    # ---------------------------------------------------------

    def add_token(
        self,
        token: "Token",
    ) -> None:
        """
        Add a token to this line.
        """

        self._add_to_collection(
            self.tokens,
            token,
        )

    # ---------------------------------------------------------

    def remove_token(
        self,
        token: "Token",
    ) -> None:
        """
        Remove a token from this line.
        """

        self._remove_from_collection(
            self.tokens,
            token,
        )

    # ---------------------------------------------------------

    def clear_tokens(
        self,
    ) -> None:
        """
        Remove all tokens.
        """

        self._clear_collection(
            self.tokens,
        )

    # ---------------------------------------------------------
    # Collection Helpers
    # ---------------------------------------------------------

    @property
    def token_count(self) -> int:
        """
        Number of tokens in this line.
        """

        return self._collection_size(
            self.tokens,
        )

    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.token_count

    # ---------------------------------------------------------

    def __iter__(self) -> Iterator["Token"]:
        return self._collection_iter(
            self.tokens,
        )

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> "Token":
        return self._collection_get(
            self.tokens,
            index,
        )

    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize the line.
        """

        data = super().to_dict()

        data["tokens"] = [

            token.to_dict()

            for token in self.tokens

        ]

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"Line("

            f"number={self.metadata.line_number}, "

            f"tokens={self.token_count})"

        )

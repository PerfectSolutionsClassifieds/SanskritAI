from __future__ import annotations

"""
SanskritAI
==========

Line

Represents a canonical line within a Paragraph.

A Line groups one or more Tokens and forms the final
container node in the Canonical Corpus Model.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token

The Line class intentionally remains lightweight.
Future linguistic services (tokenization validation,
syntax, morphology, semantic analysis, etc.) operate
on Line objects without becoming part of the model.

Version
-------
v0.3.0
"""

from typing import TYPE_CHECKING

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)
from SanskritAI.corpus.models.line_metadata import (
    LineMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.token import Token


class Line(
    ContainerNode[
        str,
        LineMetadata,
        "Token",
    ]
):
    """
    Canonical line.
    """

    def __init__(
        self,
        identifier: str,
        metadata: LineMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def tokens(self):
        """
        Alias for child tokens.
        """

        return self.children

    # ---------------------------------------------------------

    def add_token(
        self,
        token: "Token",
    ) -> None:
        """
        Add a token.
        """

        self.add_child(token)

    # ---------------------------------------------------------

    def remove_token(
        self,
        token: "Token",
    ) -> None:
        """
        Remove a token.
        """

        self.remove_child(token)

    # ---------------------------------------------------------

    @property
    def token_count(
        self,
    ) -> int:
        """
        Number of tokens.
        """

        return self.child_count

    # ---------------------------------------------------------

    @property
    def first_token(
        self,
    ) -> "Token | None":
        """
        Return the first token.
        """

        return self.first_child

    # ---------------------------------------------------------

    @property
    def last_token(
        self,
    ) -> "Token | None":
        """
        Return the last token.
        """

        return self.last_child

    # ---------------------------------------------------------
    # Semantic convenience
    # ---------------------------------------------------------

    @property
    def line_number(
        self,
    ) -> int | None:
        """
        Alias for the line number stored in metadata.
        """

        return self.metadata.line_number

    # ---------------------------------------------------------

    @property
    def language(
        self,
    ) -> str:
        """
        Alias for the language stored in metadata.
        """

        return self.metadata.language

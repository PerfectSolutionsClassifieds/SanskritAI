from __future__ import annotations

"""
SanskritAI
==========

Token

Represents the smallest canonical structural unit within the
Corpus Model.

A Token is a leaf node and therefore does NOT contain child
nodes.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token

Future lexical, morphological, syntactic, semantic,
dictionary, and AI annotations attach to Token objects
without modifying the structural hierarchy.

Version
-------
v0.3.0
"""

from SanskritAI.corpus.models.base_node import (
    BaseNode,
)

from SanskritAI.corpus.models.token_metadata import (
    TokenMetadata,
)


class Token(
    BaseNode[
        str,
        TokenMetadata,
    ]
):
    """
    Canonical token.
    """

    def __init__(
        self,
        identifier: str,
        metadata: TokenMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Semantic convenience
    # ---------------------------------------------------------

    @property
    def text(
        self,
    ) -> str:
        """
        Original token surface text.
        """

        return self.metadata.text

    # ---------------------------------------------------------

    @property
    def normalized_text(
        self,
    ) -> str:
        """
        Normalized token text.
        """

        return self.metadata.normalized_text

    # ---------------------------------------------------------

    @property
    def token_type(
        self,
    ) -> object:
        """
        Token classification.
        """

        return self.metadata.token_type

    # ---------------------------------------------------------

    @property
    def language(
        self,
    ):
        """
        Language of the token.

        Language belongs to the shared Classification object.
        """

        return self.metadata.classification.language

    # ---------------------------------------------------------

    @property
    def position(
        self,
    ) -> int | None:
        """
        Position of the token within its parent line.
        """

        return self.metadata.position

    # ---------------------------------------------------------

    @property
    def is_punctuation(
        self,
    ) -> bool:
        """
        True if this token represents punctuation.
        """

        return self.metadata.is_punctuation

    # ---------------------------------------------------------

    @property
    def is_word(
        self,
    ) -> bool:
        """
        True if this token represents a lexical word.
        """

        return self.metadata.is_word

from __future__ import annotations

"""
SanskritAI
==========

Token Builder

Builder for constructing canonical Token objects.

Version
-------
v0.1.0
"""

from typing import Self

from SanskritAI.common.identifiers.token_id import (
    TokenId,
)

from SanskritAI.corpus.builders.node_builder import (
    NodeBuilder,
)

from SanskritAI.corpus.enums.token_type import (
    TokenType,
)

from SanskritAI.corpus.models.token import (
    Token,
)

from SanskritAI.corpus.models.token_metadata import (
    TokenMetadata,
)


class TokenBuilder(
    NodeBuilder[
        Token,
        TokenMetadata,
    ]
):
    """
    Builder for Token objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Token:

        return Token(
            id=TokenId.generate(),
            metadata=TokenMetadata(),
        )

    # ---------------------------------------------------------
    # Token Content
    # ---------------------------------------------------------

    def with_text(
        self,
        text: str,
    ) -> Self:

        self._instance.text = text

        return self

    # ---------------------------------------------------------

    def with_normalized_text(
        self,
        text: str,
    ) -> Self:

        self._instance.metadata.normalized_text = text

        return self

    # ---------------------------------------------------------

    def with_token_type(
        self,
        token_type: TokenType,
    ) -> Self:

        self._instance.metadata.token_type = token_type

        return self

    # ---------------------------------------------------------

    def with_confidence(
        self,
        confidence: float,
    ) -> Self:

        self._instance.metadata.confidence = confidence

        return self

    # ---------------------------------------------------------

    def with_source_offset(
        self,
        offset: int,
    ) -> Self:

        self._instance.metadata.source_offset = offset

        return self

    # ---------------------------------------------------------

    @classmethod
    def from_token(
        cls,
        token: Token,
    ) -> "TokenBuilder":

        return cls().from_instance(token)

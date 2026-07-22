from __future__ import annotations

"""
SanskritAI
==========

Token

Canonical terminal node of the SanskritAI Corpus Model.

A Token represents the smallest structural textual unit.

Examples
--------
• Sanskrit word
• Telugu word
• English word
• punctuation
• number
• symbol

Unlike higher-level nodes, Token is a leaf node and therefore
inherits directly from BaseNode.

Version
-------
v0.1.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.common.identifiers.token_id import (
    TokenId,
)

from SanskritAI.corpus.models.base_node import (
    BaseNode,
)

from SanskritAI.corpus.models.token_metadata import (
    TokenMetadata,
)


@dataclass(slots=True)
class Token(
    BaseNode[
        TokenId,
        TokenMetadata,
    ]
):
    """
    Canonical Token node.
    """

    id: TokenId

    metadata: TokenMetadata = field(
        default_factory=TokenMetadata
    )

    # ---------------------------------------------------------
    # Lexical Content
    # ---------------------------------------------------------

    text: str = ""

    # ---------------------------------------------------------

    @property
    def normalized_text(self) -> str:
        """
        Returns normalized text if available;
        otherwise returns the original text.
        """

        return (
            self.metadata.normalized_text
            or self.text
        )

    # ---------------------------------------------------------

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the token contains no text.
        """

        return len(self.text) == 0

    # ---------------------------------------------------------

    @property
    def length(self) -> int:
        """
        Number of Unicode characters.
        """

        return len(self.text)

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the token.
        """

        data = super().to_dict()

        data.update(

            {

                "text":
                    self.text,

            }

        )

        return data

    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.text

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"Token("

            f"text={self.text!r}, "

            f"type={self.metadata.token_type.value!r})"

        )

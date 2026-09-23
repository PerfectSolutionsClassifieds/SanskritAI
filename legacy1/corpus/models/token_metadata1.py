from __future__ import annotations

"""
SanskritAI
==========

Token Metadata

Metadata describing a canonical token.

A Token represents the smallest structural textual unit within the
Canonical Corpus Model.

Examples
--------
• Sanskrit word
• Telugu word
• English word
• punctuation
• number
• symbol

Grammatical analysis is intentionally NOT stored here. It belongs
to the future annotation/morphology subsystem.

Version
-------
v0.1.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.corpus.enums.token_type import TokenType

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)


@dataclass(slots=True)
class TokenMetadata(BaseNodeMetadata):
    """
    Metadata describing a canonical token.
    """

    # ---------------------------------------------------------
    # Position
    # ---------------------------------------------------------

    token_index: int = 0

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    token_type: TokenType = TokenType.WORD

    # ---------------------------------------------------------
    # Text Normalization
    # ---------------------------------------------------------

    normalized_text: str = ""

    # ---------------------------------------------------------
    # Formatting
    # ---------------------------------------------------------

    has_leading_whitespace: bool = False

    has_trailing_whitespace: bool = False

    is_punctuation: bool = False

    is_sentence_boundary: bool = False

    # ---------------------------------------------------------
    # OCR / Import
    # ---------------------------------------------------------

    confidence: float | None = None

    source_offset: int | None = None

    # ---------------------------------------------------------

    @property
    def has_normalized_text(self) -> bool:
        """
        Returns True if a normalized representation exists.
        """

        return bool(self.normalized_text)

    # ---------------------------------------------------------

    @property
    def is_word(self) -> bool:
        """
        Returns True if this token represents a lexical word.
        """

        return self.token_type == TokenType.WORD

    # ---------------------------------------------------------

    @property
    def is_whitespace(self) -> bool:
        """
        Returns True if this token represents whitespace.
        """

        return self.token_type == TokenType.WHITESPACE

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.
        """

        data = super().to_dict()

        data.update(

            {

                "token_index":
                    self.token_index,

                "token_type":
                    self.token_type.value,

                "normalized_text":
                    self.normalized_text,

                "has_leading_whitespace":
                    self.has_leading_whitespace,

                "has_trailing_whitespace":
                    self.has_trailing_whitespace,

                "is_punctuation":
                    self.is_punctuation,

                "is_sentence_boundary":
                    self.is_sentence_boundary,

                "confidence":
                    self.confidence,

                "source_offset":
                    self.source_offset,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"TokenMetadata("

            f"index={self.token_index}, "

            f"type={self.token_type.value!r})"

        )

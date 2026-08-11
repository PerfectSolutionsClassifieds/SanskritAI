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
v0.3.1
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.corpus.enums.token_type import TokenType

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)


@dataclass(slots=True, init=False)
class TokenMetadata(BaseNodeMetadata):
    """
    Metadata describing a canonical token.

    ``position`` is the canonical internal field.

    ``token_index`` is retained as a compatibility alias because
    existing reader fixtures use that terminology.
    """

    # ---------------------------------------------------------
    # Token text
    # ---------------------------------------------------------

    text: str = ""

    normalized_text: str = ""

    # ---------------------------------------------------------
    # Position
    # ---------------------------------------------------------

    position: int | None = None

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    token_type: TokenType = TokenType.WORD

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
    # Constructor
    # ---------------------------------------------------------

    def __init__(
        self,
        *,
        identifier: str | None = None,
        text: str = "",
        normalized_text: str = "",
        position: int | None = None,
        token_index: int | None = None,
        token_type: TokenType = TokenType.WORD,
        has_leading_whitespace: bool = False,
        has_trailing_whitespace: bool = False,
        is_punctuation: bool = False,
        is_sentence_boundary: bool = False,
        confidence: float | None = None,
        source_offset: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Construct TokenMetadata.

        ``token_index`` is accepted as a compatibility alias for
        ``position``.
        """

        # -----------------------------------------------------
        # Resolve position / token_index
        # -----------------------------------------------------

        if (
            position is not None
            and token_index is not None
            and position != token_index
        ):
            raise ValueError(
                "position and token_index must refer to "
                "the same token position"
            )

        resolved_position = (
            position
            if position is not None
            else token_index
        )

        # -----------------------------------------------------
        # Initialize BaseNodeMetadata
        # -----------------------------------------------------

        BaseNodeMetadata.__init__(
            self,
            identifier=identifier,
            **kwargs,
        )

        # -----------------------------------------------------
        # Token text
        # -----------------------------------------------------

        self.text = text
        self.normalized_text = normalized_text

        # -----------------------------------------------------
        # Position
        # -----------------------------------------------------

        self.position = resolved_position

        # -----------------------------------------------------
        # Classification
        # -----------------------------------------------------

        self.token_type = token_type

        # -----------------------------------------------------
        # Formatting
        # -----------------------------------------------------

        self.has_leading_whitespace = (
            has_leading_whitespace
        )

        self.has_trailing_whitespace = (
            has_trailing_whitespace
        )

        self.is_punctuation = is_punctuation

        self.is_sentence_boundary = (
            is_sentence_boundary
        )

        # -----------------------------------------------------
        # OCR / Import
        # -----------------------------------------------------

        self.confidence = confidence

        self.source_offset = source_offset

    # ---------------------------------------------------------
    # Compatibility alias
    # ---------------------------------------------------------

    @property
    def token_index(self) -> int | None:
        """
        Compatibility alias for ``position``.
        """

        return self.position

    @token_index.setter
    def token_index(
        self,
        value: int | None,
    ) -> None:

        self.position = value

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_normalized_text(self) -> bool:
        """
        Returns True if normalized text exists.
        """

        return bool(self.normalized_text)

    # ---------------------------------------------------------

    @property
    def is_word(self) -> bool:
        """
        True if this token represents a lexical word.
        """

        return self.token_type == TokenType.WORD

    # ---------------------------------------------------------

    @property
    def is_whitespace(self) -> bool:
        """
        True if this token represents whitespace.
        """

        return self.token_type == TokenType.WHITESPACE

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.
        """

        data = BaseNodeMetadata.to_dict(self)

        data.update(
            {
                "text": self.text,

                "normalized_text":
                    self.normalized_text,

                "position":
                    self.position,

                "token_index":
                    self.position,

                "token_type":
                    self.token_type.value,

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
            "TokenMetadata("
            f"identifier={self.identifier!r}, "
            f"text={self.text!r}, "
            f"position={self.position}, "
            f"type={self.token_type.value!r})"
        )

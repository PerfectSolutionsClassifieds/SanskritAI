from __future__ import annotations

"""
SanskritAI
==========

Tokenizer Token

Immutable lexical unit produced by the tokenizer.

A TokenizerToken represents the smallest recognized unit of
source text before parsing, grammatical analysis or semantic
interpretation.

TokenizerToken is intentionally language-independent and forms
the canonical output of the Tokenizer Kernel.

Pipeline
--------

Raw Text
    ↓
Tokenizer
    ↓
TokenizerToken
    ↓
Parser
    ↓
Records

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.tokenizers.token_position import TokenPosition
from SanskritAI.core.tokenizers.token_type import TokenType


@dataclass(slots=True, frozen=True)
class TokenizerToken:
    """
    Immutable lexical token produced by the tokenizer.
    """

    # ---------------------------------------------------------
    # Token content
    # ---------------------------------------------------------

    text: str

    token_type: TokenType

    position: TokenPosition

    # ---------------------------------------------------------
    # Optional normalized representation
    # ---------------------------------------------------------

    normalized: str = ""

    # ---------------------------------------------------------
    # Convenience properties
    # ---------------------------------------------------------

    @property
    def value(self) -> str:
        """
        Preferred lexical representation.

        Returns the normalized form when available;
        otherwise returns the original text.
        """
        return self.normalized or self.text

    @property
    def is_content(self) -> bool:
        """
        Returns True if this token represents textual content.
        """
        return self.token_type.is_content

    @property
    def is_whitespace(self) -> bool:
        """
        Returns True if this token represents whitespace.
        """
        return self.token_type.is_whitespace

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if this token terminates tokenization.
        """
        return self.token_type.is_terminal

    @property
    def length(self) -> int:
        """
        Length of the token text.
        """
        return len(self.text)

    def matches(
        self,
        value: str,
        *,
        normalized: bool = True,
        case_sensitive: bool = True,
    ) -> bool:
        """
        Compare the token against a string.

        Parameters
        ----------
        value:
            Text to compare against.

        normalized:
            Compare against the normalized value when available.

        case_sensitive:
            Perform a case-sensitive comparison.
        """
        token_value = self.value if normalized else self.text

        if case_sensitive:
            return token_value == value

        return token_value.casefold() == value.casefold()

    def __str__(self) -> str:
        """
        Human-readable representation.
        """
        return (
            f"{self.token_type.name}"
            f"('{self.text}') "
            f"@ {self.position}"
        )

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """
        return (
            f"TokenizerToken("
            f"text={self.text!r}, "
            f"type={self.token_type.name}, "
            f"position={self.position!r})"
        )

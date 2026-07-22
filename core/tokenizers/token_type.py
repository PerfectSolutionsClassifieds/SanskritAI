from __future__ import annotations

"""
SanskritAI
==========

Tokenizer Token Types

Defines the lexical categories recognized by the tokenizer.

These token types represent surface-level lexical units only.
They intentionally avoid any grammatical or semantic
classification.

Grammatical analysis is performed later by the Morphological
Engine.

Version
-------
v0.6.0
"""

from enum import Enum, auto


class TokenType(Enum):
    """
    Enumeration of tokenizer token types.

    These values describe the lexical form of text before
    parsing or grammatical analysis.
    """

    # ---------------------------------------------------------
    # Textual content
    # ---------------------------------------------------------

    WORD = auto()

    NUMBER = auto()

    SYMBOL = auto()

    PUNCTUATION = auto()

    # ---------------------------------------------------------
    # Whitespace
    # ---------------------------------------------------------

    WHITESPACE = auto()

    NEWLINE = auto()

    TAB = auto()

    # ---------------------------------------------------------
    # Delimiters
    # ---------------------------------------------------------

    DELIMITER = auto()

    # ---------------------------------------------------------
    # Structural
    # ---------------------------------------------------------

    COMMENT = auto()

    MARKUP = auto()

    METADATA = auto()

    # ---------------------------------------------------------
    # Special
    # ---------------------------------------------------------

    UNKNOWN = auto()

    EOF = auto()

    ERROR = auto()

    # ---------------------------------------------------------

    @property
    def is_content(self) -> bool:
        """
        Returns True if the token represents textual content.
        """
        return self in {
            TokenType.WORD,
            TokenType.NUMBER,
            TokenType.SYMBOL,
        }

    @property
    def is_whitespace(self) -> bool:
        """
        Returns True if the token represents whitespace.
        """
        return self in {
            TokenType.WHITESPACE,
            TokenType.NEWLINE,
            TokenType.TAB,
        }

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if the token terminates tokenization.
        """
        return self in {
            TokenType.EOF,
            TokenType.ERROR,
        }

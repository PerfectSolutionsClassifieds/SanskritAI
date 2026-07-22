from __future__ import annotations

"""
SanskritAI
==========

Token Type Enumeration

Canonical token classifications.

These values are intentionally generic so that the same model can
represent Sanskrit, Telugu, English and other languages.

Version
-------
v0.1.0
"""

from enum import Enum


class TokenType(str, Enum):
    """
    Canonical token classifications.
    """

    UNKNOWN = "unknown"

    WORD = "word"

    NUMBER = "number"

    SYMBOL = "symbol"

    PUNCTUATION = "punctuation"

    WHITESPACE = "whitespace"

    NEWLINE = "newline"

    MARKUP = "markup"

    ABBREVIATION = "abbreviation"

    EMOJI = "emoji"

    SPECIAL = "special"

    # ---------------------------------------------------------

    @classmethod
    def from_string(
        cls,
        value: str | None,
    ) -> "TokenType":

        if not value:
            return cls.UNKNOWN

        normalized = value.strip().lower()

        for item in cls:

            if item.value == normalized:
                return item

        return cls.UNKNOWN

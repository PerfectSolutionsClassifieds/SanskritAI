from __future__ import annotations

"""
SanskritAI
==========

Lexical Language

Compatibility enum for lexical records and builders.

The lexical layer owns the public lexical-facing type while
remaining intentionally lightweight.

Version
-------
v0.4.1
"""

from enum import Enum


class Language(str, Enum):
    """
    Language identifiers used by lexical records.

    Sanskrit is the default language of SanskritAI.
    """

    UNKNOWN = "unknown"

    SANSKRIT = "sanskrit"

    ENGLISH = "english"

    HINDI = "hindi"

    TELUGU = "telugu"

    TAMIL = "tamil"

    KANNADA = "kannada"

    MALAYALAM = "malayalam"

    BENGALI = "bengali"

    MARATHI = "marathi"

    PALI = "pali"

    PRAKRIT = "prakrit"

from __future__ import annotations

"""
SanskritAI
==========

Language Enumeration

Canonical language identifiers used throughout
the SanskritAI corpus model.

Version
-------
v0.1.0
"""

from enum import StrEnum, auto


class Language(StrEnum):
    """
    Supported languages.
    """

    UNKNOWN = auto()

    SANSKRIT = auto()

    VEDIC_SANSKRIT = auto()

    CLASSICAL_SANSKRIT = auto()

    PRAKRIT = auto()

    PALI = auto()

    HINDI = auto()

    TELUGU = auto()

    TAMIL = auto()

    KANNADA = auto()

    MALAYALAM = auto()

    ODIA = auto()

    BENGALI = auto()

    MARATHI = auto()

    GUJARATI = auto()

    ENGLISH = auto()

    MIXED = auto()

from __future__ import annotations

"""
SanskritAI
==========

Script Enumeration

Canonical writing systems and transliteration
schemes supported by SanskritAI.

Version
-------
v0.1.0
"""

from enum import StrEnum, auto


class Script(StrEnum):
    """
    Writing systems and transliteration schemes.
    """

    UNKNOWN = auto()

    DEVANAGARI = auto()

    TELUGU = auto()

    KANNADA = auto()

    TAMIL = auto()

    MALAYALAM = auto()

    BENGALI = auto()

    GUJARATI = auto()

    ODIA = auto()

    GRANTHA = auto()

    SHARADA = auto()

    IAST = auto()

    ISO15919 = auto()

    HARVARD_KYOTO = auto()

    ITRANS = auto()

    SLP1 = auto()

    VELTHUIS = auto()

    WX = auto()

    ROMAN = auto()

    MIXED = auto()

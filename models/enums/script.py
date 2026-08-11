
"""
SanskritAI
==========

Module:
    models.enums.script

Description:
    Supported writing systems and transliteration scripts.

Version:
    v0.3.0 Final
"""

from enum import Enum


class Script(Enum):
    """
    Supported writing systems and transliteration schemes.

    The enum values are canonical human-readable identifiers.
    """

    UNKNOWN = "Unknown"

    DEVANAGARI = "Devanagari"

    TELUGU = "Telugu"

    IAST = "IAST"

    ITRANS = "ITRANS"

    HK = "Harvard-Kyoto"

    SLP1 = "SLP1"

    WX = "WX"

    ISO15919 = "ISO 15919"

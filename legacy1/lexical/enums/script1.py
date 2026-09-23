from __future__ import annotations

"""
SanskritAI
==========

Lexical Script

Compatibility enum for lexical records and builders.

Version
-------
v0.4.1
"""

from enum import Enum


class Script(str, Enum):
    """
    Script identifiers used by lexical records.
    """

    UNKNOWN = "unknown"

    DEVANAGARI = "devanagari"

    IAST = "iast"

    TELUGU = "telugu"

    TAMIL = "tamil"

    KANNADA = "kannada"

    MALAYALAM = "malayalam"

    BENGALI = "bengali"

    GUJARATI = "gujarati"

    GURMUKHI = "gurmukhi"

    ORIYA = "oriya"

    GRANtha = "grantha"

    ROMAN = "roman"

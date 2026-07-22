from __future__ import annotations

"""
SanskritAI
==========

Corpus Type Enumeration

Defines the canonical classification of a corpus.

Version
-------
v0.1.0
"""

from enum import StrEnum, auto


class CorpusType(StrEnum):
    """
    Canonical corpus categories.
    """

    UNKNOWN = auto()

    VEDA = auto()

    VEDANGA = auto()

    UPANISHAD = auto()

    ITIHASA = auto()

    PURANA = auto()

    AGAMA = auto()

    TANTRA = auto()

    SMRITI = auto()

    DHARMASHASTRA = auto()

    KAVYA = auto()

    NATAKA = auto()

    SUBHASHITA = auto()

    STOTRA = auto()

    SUTRA = auto()

    BHASHYA = auto()

    TIKA = auto()

    VYAKARANA = auto()

    KOSHA = auto()

    DICTIONARY = auto()

    COMMENTARY = auto()

    MANUSCRIPT = auto()

    LEXICON = auto()

    MIXED = auto()

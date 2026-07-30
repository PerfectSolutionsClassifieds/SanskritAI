from __future__ import annotations

"""
SanskritAI
==========

Phoneme Classifier

Provides semantic classification of Sanskrit phonemes.

Version
-------
v1.1.0
"""

from SanskritAI.domain.phonology.anusvara import Anusvara
from SanskritAI.domain.phonology.consonant import Consonant
from SanskritAI.domain.phonology.jihvamuliya import Jihvamuliya
from SanskritAI.domain.phonology.non_alphabetic_ayogavaha_phoneme import (
    NonAlphabeticAyogavahaPhoneme,
)
from SanskritAI.domain.phonology.phoneme import Phoneme
from SanskritAI.domain.phonology.phoneme_property import (
    AC,
    AYOGAVAHA,
    DIRGHA,
    HRASVA,
    JIHVAMULIYA,
    KANTHYA,
    OSTHYA,
    UPADHMANIYA,
)
from SanskritAI.domain.phonology.upadhmaniya import Upadhmaniya
from SanskritAI.domain.phonology.vowel import Vowel
from SanskritAI.domain.phonology.visarga import Visarga


class PhonemeClassifier:
    """
    Provides semantic classification for Sanskrit phonemes.
    """

    @staticmethod
    def is_ac(phoneme: Phoneme) -> bool:
        return phoneme.has_any_property(AC) or isinstance(phoneme, Vowel)

    @staticmethod
    def is_hal(phoneme: Phoneme) -> bool:
        return isinstance(phoneme, Consonant)

    @staticmethod
    def is_ayogavaha(phoneme: Phoneme) -> bool:
        return isinstance(phoneme, NonAlphabeticAyogavahaPhoneme)

    @staticmethod
    def is_visarga(phoneme: Phoneme) -> bool:
        return isinstance(phoneme, Visarga)

    @staticmethod
    def is_anusvara(phoneme: Phoneme) -> bool:
        return isinstance(phoneme, Anusvara)

    @staticmethod
    def is_jihvamuliya(phoneme: Phoneme) -> bool:
        return isinstance(phoneme, Jihvamuliya) or phoneme.has_property(JIHVAMULIYA)

    @staticmethod
    def is_upadhmaniya(phoneme: Phoneme) -> bool:
        return isinstance(phoneme, Upadhmaniya) or phoneme.has_property(UPADHMANIYA)

    @staticmethod
    def is_short_vowel(phoneme: Phoneme) -> bool:
        return phoneme.has_property(HRASVA)

    @staticmethod
    def is_long_vowel(phoneme: Phoneme) -> bool:
        return phoneme.has_property(DIRGHA)

    @staticmethod
    def is_kanthya(phoneme: Phoneme) -> bool:
        return phoneme.has_property(KANTHYA)

    @staticmethod
    def is_osthya(phoneme: Phoneme) -> bool:
        return phoneme.has_property(OSTHYA)

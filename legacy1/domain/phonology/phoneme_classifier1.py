from __future__ import annotations

"""
SanskritAI
==========

Phoneme Classifier

Provides semantic classification of Sanskrit phonemes.

The classifier encapsulates traditional Sanskrit
phonological knowledge and should be the only component
responsible for determining phonological classes.

Future Sandhi, Grammar and Morphology kernels should depend
on this classifier rather than performing direct Unicode
comparisons.

Hierarchy
---------

PhonemeSpecification
        │
        ▼
PhonemeFactory
        │
        ▼
PhonemeInventory
        │
        ▼
PhonemeClassifier
        │
        ▼
Sandhi Rules

Version
-------
v1.0.0
"""

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)

from SanskritAI.domain.phonology.vowel import (
    Vowel,
)

from SanskritAI.domain.phonology.consonant import (
    Consonant,
)

from SanskritAI.domain.phonology.non_alphabetic_ayogavaha_phoneme import (
    NonAlphabeticAyogavahaPhoneme,
)


class PhonemeClassifier:
    """
    Provides semantic classification for Sanskrit phonemes.
    """

    # ---------------------------------------------------------
    # Primary Paninian Classes
    # ---------------------------------------------------------

    @staticmethod
    def is_ac(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the phoneme belongs to
        अच् (vowels).
        """

        return isinstance(
            phoneme,
            Vowel,
        )

    # ---------------------------------------------------------

    @staticmethod
    def is_hal(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the phoneme belongs to
        हल् (consonants).
        """

        return isinstance(
            phoneme,
            Consonant,
        )

    # ---------------------------------------------------------

    @staticmethod
    def is_ayogavaha(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the phoneme belongs to
        अयोगवाह.
        """

        return isinstance(
            phoneme,
            NonAlphabeticAyogavahaPhoneme,
        )

    # ---------------------------------------------------------
    # Secondary Paninian Classes
    #
    # These currently act as placeholders.
    # They will become fully data-driven once the
    # complete Sanskrit phoneme inventory has been
    # introduced.
    # ---------------------------------------------------------

    @staticmethod
    def is_antastha(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the phoneme belongs to
        अन्तःस्थ.

        TODO:
            Implement from canonical phoneme
            specification.
        """

        return False

    # ---------------------------------------------------------

    @staticmethod
    def is_ushman(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the phoneme belongs to
        ऊष्मन्.

        TODO:
            Implement from canonical phoneme
            specification.
        """

        return False

    # ---------------------------------------------------------

    @staticmethod
    def is_varga(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the phoneme belongs to one
        of the five consonant vargas.

        TODO:
            Implement from canonical phoneme
            specification.
        """

        return False

    # ---------------------------------------------------------

    @staticmethod
    def is_short_vowel(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the vowel is short
        (ह्रस्व).

        TODO:
            Implement from canonical phoneme
            specification.
        """

        return False

    # ---------------------------------------------------------

    @staticmethod
    def is_long_vowel(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the vowel is long
        (दीर्घ).

        TODO:
            Implement from canonical phoneme
            specification.
        """

        return False

    # ---------------------------------------------------------

    @staticmethod
    def is_pluta(
        phoneme: Phoneme,
    ) -> bool:
        """
        Determines whether the vowel is pluta.

        Reserved for future Vedic support.
        """

        return False

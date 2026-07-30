from __future__ import annotations

"""
SanskritAI
==========

Non Alphabetic Ayogavaha Phoneme

Defines the abstract foundation for Sanskrit phonological
units traditionally classified as Ayogavāhas (अयोगवाहाः).

Ayogavāhas are phonetic entities which participate in
phonological transformations yet are neither vowels
(स्वराः) nor consonants (व्यञ्जनानि).

Current subclasses
------------------

• Visarga (ः)

• Anusvāra (ं)

Future subclasses
-----------------

• Jihvāmūlīya

• Upadhmānīya

This class intentionally combines the English architectural
description ("Non Alphabetic Phoneme") with the traditional
Sanskrit grammatical classification ("Ayogavāha").

Hierarchy
---------

Phoneme
    │
    ├── Vowel
    ├── Consonant
    └── NonAlphabeticAyogavahaPhoneme
            │
            ├── Visarga
            └── Anusvara

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)


class NonAlphabeticAyogavahaPhoneme(
    Phoneme,
    ABC,
):
    """
    Abstract Ayogavāha phoneme.
    """

    @property
    def is_non_alphabetic(self) -> bool:
        return True

    @property
    def is_ayogavaha(self) -> bool:
        """
        Indicates that this phoneme belongs to the
        traditional Ayogavāha category.
        """
        return True

    @property
    def display_name(self) -> str:
        return "Non Alphabetic Ayogavaha Phoneme"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Abstract Sanskrit Ayogavāha phoneme."
        )

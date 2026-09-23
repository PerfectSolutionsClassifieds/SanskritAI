from __future__ import annotations

"""
SanskritAI
==========

Non Alphabetic Phoneme

Abstract superclass representing Sanskrit phonological units
which are neither vowels nor consonants.

Examples
--------

Visarga

Anusvāra

Future

Jihvāmūlīya

Upadhmānīya

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
    Abstract non-alphabetic phoneme.
    """

    @property
    def is_non_alphabetic(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return "Non Alphabetic Phoneme"

    @property
    def display_description(self) -> str:
        return (
            "Abstract Sanskrit non-alphabetic phoneme."
        )

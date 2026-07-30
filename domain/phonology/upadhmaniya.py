from __future__ import annotations

"""
SanskritAI
==========

Upadhmānīya

Defines the phonological Ayogavāha phoneme used before
labial consonants in traditional Sanskrit phonology.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.phonology.non_alphabetic_ayogavaha_phoneme import (
    NonAlphabeticAyogavahaPhoneme,
)


@dataclass(frozen=True, slots=True)
class Upadhmaniya(
    NonAlphabeticAyogavahaPhoneme,
):
    """
    Sanskrit Upadhmānīya phoneme.
    """

    @property
    def display_name(self) -> str:
        return "Upadhmaniya"

    @property
    def display_text(self) -> str:
        return "ᳶ"

    @property
    def display_description(self) -> str:
        return "Upadhmānīya Ayogavāha phoneme."

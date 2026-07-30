from __future__ import annotations

"""
SanskritAI

Vowel (Svara)
"""

from dataclasses import dataclass

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)


@dataclass(frozen=True, slots=True)
class Vowel(
    Phoneme,
):
    """
    Sanskrit vowel.
    """

    @property
    def is_vowel(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return "Vowel"

from __future__ import annotations

"""
SanskritAI

Consonant (Vyañjana)
"""

from dataclasses import dataclass

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)


@dataclass(frozen=True, slots=True)
class Consonant(
    Phoneme,
):
    """
    Sanskrit consonant.
    """

    @property
    def is_consonant(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return "Consonant"

from __future__ import annotations

"""
SanskritAI
==========

Lakara

Canonical Sanskrit verbal tense/mood category.

Lakara belongs to the verbal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.verbal_category import VerbalCategory


@dataclass(frozen=True, slots=True)
class Lakara(VerbalCategory):
    """
    Canonical Sanskrit tense/mood category.
    """

    identifier: str = "lakara"
    sanskrit_name: str = "लकार"
    english_name: str = "Tense / Mood"
    abbreviation: str = "LKR"
    description: str = "Verbal tense and mood category."
    order: int = 5

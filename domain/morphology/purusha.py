from __future__ import annotations

"""
SanskritAI
==========

Purusha

Canonical Sanskrit verbal person category.

Purusha belongs to the verbal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.verbal_category import VerbalCategory


@dataclass(frozen=True, slots=True)
class Purusha(VerbalCategory):
    """
    Canonical Sanskrit person category.
    """

    identifier: str = "purusha"
    sanskrit_name: str = "पुरुष"
    english_name: str = "Person"
    abbreviation: str = "PRS"
    description: str = "Verbal grammatical person."
    order: int = 4

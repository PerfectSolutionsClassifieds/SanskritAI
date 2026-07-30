from __future__ import annotations

"""
SanskritAI
==========

Prayoga

Canonical Sanskrit verbal voice/usage category.

Prayoga belongs to the verbal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.verbal_category import VerbalCategory


@dataclass(frozen=True, slots=True)
class Prayoga(VerbalCategory):
    """
    Canonical Sanskrit voice/usage category.
    """

    identifier: str = "prayoga"
    sanskrit_name: str = "प्रयोग"
    english_name: str = "Voice / Usage"
    abbreviation: str = "PRY"
    description: str = "Verbal usage or voice category."
    order: int = 7

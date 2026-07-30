from __future__ import annotations

"""
SanskritAI
==========

Vibhakti

Canonical Sanskrit nominal case category.

Vibhakti belongs to the nominal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.nominal_category import NominalCategory


@dataclass(frozen=True, slots=True)
class Vibhakti(NominalCategory):
    """
    Canonical Sanskrit case category.
    """

    identifier: str = "vibhakti"
    sanskrit_name: str = "विभक्ति"
    english_name: str = "Case"
    abbreviation: str = "VBH"
    description: str = "Nominal grammatical case."
    order: int = 1

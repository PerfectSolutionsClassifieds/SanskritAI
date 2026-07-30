from __future__ import annotations

"""
SanskritAI
==========

Vacana

Canonical Sanskrit nominal number category.

Vacana belongs to the nominal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.nominal_category import NominalCategory


@dataclass(frozen=True, slots=True)
class Vacana(NominalCategory):
    """
    Canonical Sanskrit number category.
    """

    identifier: str = "vacana"
    sanskrit_name: str = "वचन"
    english_name: str = "Number"
    abbreviation: str = "VAC"
    description: str = "Nominal grammatical number."
    order: int = 2

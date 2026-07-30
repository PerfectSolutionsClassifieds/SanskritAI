from __future__ import annotations

"""
SanskritAI
==========

Linga

Canonical Sanskrit nominal gender category.

Linga belongs to the nominal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.nominal_category import NominalCategory


@dataclass(frozen=True, slots=True)
class Linga(NominalCategory):
    """
    Canonical Sanskrit gender category.
    """

    identifier: str = "linga"
    sanskrit_name: str = "लिङ्ग"
    english_name: str = "Gender"
    abbreviation: str = "LIN"
    description: str = "Nominal grammatical gender."
    order: int = 3

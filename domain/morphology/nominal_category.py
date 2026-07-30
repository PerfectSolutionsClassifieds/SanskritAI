from __future__ import annotations

"""
SanskritAI
==========

Nominal Category

Defines the abstract foundation for all grammatical
categories associated with Sanskrit nominal forms.

Nominal categories include:

• Vibhakti
• Vacana
• Linga

These categories describe nouns, pronouns, adjectives,
participles and other nominal forms.

Hierarchy
---------

GrammaticalCategory
        │
        └── NominalCategory
                ├── Vibhakti
                ├── Vacana
                └── Linga

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.morphology.grammatical_category import (
    GrammaticalCategory,
)


class NominalCategory(
    GrammaticalCategory,
    ABC,
):
    """
    Abstract base class for nominal grammatical categories.
    """

    @property
    def grammatical_domain(self) -> str:
        """
        Returns the grammatical domain.

        Always:

            nominal
        """

        return "nominal"

    @property
    def is_nominal(self) -> bool:
        return True

    @property
    def is_verbal(self) -> bool:
        return False

from __future__ import annotations

"""
SanskritAI
==========

Verbal Category

Defines the abstract foundation for all grammatical
categories associated with Sanskrit verbal forms.

Verbal categories include:

• Lakara
• Purusha
• Pada
• Prayoga

Hierarchy
---------

GrammaticalCategory
        │
        └── VerbalCategory
                ├── Lakara
                ├── Purusha
                ├── Pada
                └── Prayoga

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.morphology.grammatical_category import (
    GrammaticalCategory,
)


class VerbalCategory(
    GrammaticalCategory,
    ABC,
):
    """
    Abstract base class for verbal grammatical categories.
    """

    @property
    def grammatical_domain(self) -> str:
        """
        Returns the grammatical domain.

        Always:

            verbal
        """

        return "verbal"

    @property
    def is_nominal(self) -> bool:
        return False

    @property
    def is_verbal(self) -> bool:
        return True

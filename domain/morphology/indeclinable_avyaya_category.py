from __future__ import annotations

"""
SanskritAI
==========

Indeclinable Avyaya Category

Defines the abstract foundation for all Sanskrit
indeclinable (अव्यय) grammatical categories.

In the traditional Sanskrit grammatical system, avyayas
are words that do not undergo inflection for:

    • Vibhakti
    • Vacana
    • Liṅga

Examples
--------

च

वा

हि

एव

अपि

न

उत

नमः

Relationship
------------

GrammaticalCategory
        │
        └── IndeclinableAvyayaCategory
                │
                ├── Nipata
                ├── Upasarga
                ├── Avyaya
                ├── Particle
                └── IndeclinableExpression

This abstraction intentionally models the traditional
Sanskrit grammatical concept rather than a modern NLP
feature.

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.morphology.grammatical_category import (
    GrammaticalCategory,
)


class IndeclinableAvyayaCategory(
    GrammaticalCategory,
    ABC,
):
    """
    Abstract foundation for all indeclinable Sanskrit
    grammatical categories.
    """

    @property
    def grammatical_domain(self) -> str:
        """
        Returns the grammatical domain.

        Always:

            indeclinable
        """
        return "indeclinable"

    @property
    def sanskrit_domain(self) -> str:
        """
        Traditional Sanskrit grammatical domain.
        """
        return "अव्यय"

    @property
    def is_nominal(self) -> bool:
        return False

    @property
    def is_verbal(self) -> bool:
        return False

    @property
    def is_indeclinable(self) -> bool:
        return True

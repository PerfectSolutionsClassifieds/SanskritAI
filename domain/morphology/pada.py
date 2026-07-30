from __future__ import annotations

"""
SanskritAI
==========

Pada

Canonical Sanskrit verbal pada category.

Pada belongs to the verbal grammatical domain and is a
concrete instantiation of GrammaticalCategory.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.verbal_category import VerbalCategory


@dataclass(frozen=True, slots=True)
class Pada(VerbalCategory):
    """
    Canonical Sanskrit verbal pada category.
    """

    identifier: str = "pada"
    sanskrit_name: str = "पद"
    english_name: str = "Verb Ending / Voice"
    abbreviation: str = "PAD"
    description: str = "Verbal pada category."
    order: int = 6

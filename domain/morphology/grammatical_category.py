from __future__ import annotations

"""
SanskritAI
==========

Grammatical Category

Defines the canonical immutable foundation for all Sanskrit
grammatical categories.

Every grammatical category (Vibhakti, Vacana, Liṅga,
Puruṣa, Lakāra, Pada, Prayoga, etc.) derives from this
base class.

This class intentionally models only the grammatical
category itself and remains independent of any parser,
analysis engine, or linguistic theory.

Hierarchy
---------

GrammaticalCategory
        │
        ├── Vibhakti
        ├── Vacana
        ├── Linga
        ├── Purusha
        ├── Lakara
        ├── Pada
        └── Prayoga

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class GrammaticalCategory(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable grammatical category.
    """

    identifier: str

    sanskrit_name: str

    english_name: str

    abbreviation: str = ""

    description: str = ""

    order: int = 0

    @property
    def display_name(self) -> str:
        return self.sanskrit_name

    @property
    def display_text(self) -> str:
        if self.english_name:
            return (
                f"{self.sanskrit_name}"
                f" ({self.english_name})"
            )

        return self.sanskrit_name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_abbreviation(self) -> bool:
        return bool(self.abbreviation)

    @property
    def has_description(self) -> bool:
        return bool(self.description)

    def __str__(self) -> str:
        return self.display_text

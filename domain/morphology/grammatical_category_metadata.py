from __future__ import annotations

"""
SanskritAI
==========

Grammatical Category Metadata

Defines immutable metadata shared by all canonical Sanskrit
grammatical categories.

Relationship
------------

GrammaticalCategoryMetadata
            │
            ▼
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
class GrammaticalCategoryMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing a grammatical category.
    """

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

    def __str__(self) -> str:
        return self.display_text

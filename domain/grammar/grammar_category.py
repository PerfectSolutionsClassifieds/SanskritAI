from __future__ import annotations

"""
SanskritAI
==========

Grammar Category

Defines the canonical immutable foundation for grammar-domain
categories in SanskritAI.

GrammarCategory is the shared base object for grammar-specific
concepts such as:

- Grammar roles
- Grammar relations
- Grammar features
- Grammar rules
- Grammar annotations

The class is intentionally domain-level and does not encode any
specific grammatical theory beyond being a canonical category
representation.

Hierarchy
---------

GrammarCategory
        │
        ├── GrammarRole
        ├── GrammarRelation
        ├── GrammarFeature
        └── GrammarRule

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class GrammarCategory(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable grammar category.
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
            return f"{self.sanskrit_name} ({self.english_name})"
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

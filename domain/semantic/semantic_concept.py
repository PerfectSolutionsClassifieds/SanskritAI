from __future__ import annotations

"""
SanskritAI
==========

Semantic Concept

Represents a reusable semantic concept in the Semantic Kernel.

A SemanticConcept is a stable meaning unit that can be linked
to upstream analysis outputs, semantic relations, and future
ontology structures.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class SemanticConcept(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic concept.
    """

    identifier: str

    name: str

    gloss: str = ""

    category: str = ""

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        if self.gloss:
            return f"{self.name} ({self.gloss})"
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_gloss(self) -> bool:
        return bool(self.gloss)

    @property
    def has_category(self) -> bool:
        return bool(self.category)

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Semantic Frame

Represents a structured meaning frame built from concepts and
relations.

The frame is the first truly structured meaning object in the
Semantic Kernel and can later support:
    • predicate-argument structure
    • event frames
    • role labeling
    • ontology linking

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.semantic.semantic_concept import SemanticConcept
from SanskritAI.domain.semantic.semantic_relation import SemanticRelation


@dataclass(frozen=True, slots=True)
class SemanticFrame(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic frame.
    """

    identifier: str

    label: str

    concepts: tuple[SemanticConcept, ...] = field(default_factory=tuple)

    relations: tuple[SemanticRelation, ...] = field(default_factory=tuple)

    summary: str = ""

    confidence: float = 1.0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.label

    @property
    def display_text(self) -> str:
        return self.label

    @property
    def display_description(self) -> str:
        return self.summary or self.notes

    @property
    def concept_count(self) -> int:
        return len(self.concepts)

    @property
    def relation_count(self) -> int:
        return len(self.relations)

    @property
    def has_concepts(self) -> bool:
        return self.concept_count > 0

    @property
    def has_relations(self) -> bool:
        return self.relation_count > 0

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    @property
    def first_concept(self) -> SemanticConcept | None:
        if not self.concepts:
            return None
        return self.concepts[0]

    @property
    def first_relation(self) -> SemanticRelation | None:
        if not self.relations:
            return None
        return self.relations[0]

    def __iter__(self) -> Iterator[SemanticConcept]:
        return iter(self.concepts)

    def __len__(self) -> int:
        return len(self.concepts)

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Semantic Relation

Represents a relation between semantic concepts.

Examples:
    • agent-of
    • patient-of
    • modifies
    • derives-from
    • part-of
    • means

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.semantic.semantic_concept import SemanticConcept


@dataclass(frozen=True, slots=True)
class SemanticRelation(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic relation.
    """

    identifier: str

    relation: str

    source: SemanticConcept

    target: SemanticConcept

    confidence: float = 1.0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.relation

    @property
    def display_text(self) -> str:
        return f"{self.source.name} —{self.relation}→ {self.target.name}"

    @property
    def display_description(self) -> str:
        return self.notes

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text

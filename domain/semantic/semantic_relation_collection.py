from __future__ import annotations

"""
SanskritAI
==========

Semantic Relation Collection

Immutable ordered collection of SemanticRelation objects.

The collection provides small, reusable value-object semantics
for the Semantic Kernel and Semantic Repository.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.semantic.semantic_relation import SemanticRelation


@dataclass(frozen=True, slots=True)
class SemanticRelationCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of semantic relations.
    """

    relations: tuple[SemanticRelation, ...] = field(
        default_factory=tuple
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Semantic Relations"

    @property
    def display_text(self) -> str:
        return f"{len(self.relations)} relations"

    @property
    def display_description(self) -> str:
        return "Immutable collection of semantic relations."

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.relations)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> SemanticRelation | None:
        if self.is_empty:
            return None

        return self.relations[0]

    # ---------------------------------------------------------
    # Immutable operations
    # ---------------------------------------------------------

    def add(
        self,
        relation: SemanticRelation,
    ) -> "SemanticRelationCollection":
        return SemanticRelationCollection(
            relations=self.relations + (relation,)
        )

    def extend(
        self,
        other: "SemanticRelationCollection",
    ) -> "SemanticRelationCollection":
        return SemanticRelationCollection(
            relations=self.relations + other.relations
        )

    # ---------------------------------------------------------
    # Collection protocol
    # ---------------------------------------------------------

    def __iter__(self) -> Iterator[SemanticRelation]:
        return iter(self.relations)

    def __len__(self) -> int:
        return len(self.relations)

    def __getitem__(self, index: int) -> SemanticRelation:
        return self.relations[index]

    def __str__(self) -> str:
        return self.display_text

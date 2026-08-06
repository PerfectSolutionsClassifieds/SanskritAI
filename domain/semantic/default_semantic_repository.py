from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Repository

Default in-memory implementation.

Initially empty until canonical semantic knowledge
is imported.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.semantic.semantic_repository import (
    SemanticRepository,
)

from SanskritAI.domain.semantic.semantic_relation import (
    SemanticRelation,
)

from SanskritAI.domain.semantic.semantic_relation_collection import (
    SemanticRelationCollection,
)


@dataclass(frozen=True, slots=True)
class DefaultSemanticRepository(
    SemanticRepository,
):
    """
    Default semantic repository.
    """

    _relations: SemanticRelationCollection = (
        SemanticRelationCollection()
    )

    def get(
        self,
        identifier: str,
    ) -> SemanticRelation | None:

        for relation in self._relations:
            if relation.identifier == identifier:
                return relation

        return None

    def search(
        self,
        query: str,
    ) -> SemanticRelationCollection:

        query = query.lower()

        return SemanticRelationCollection(
            relations=tuple(
                relation
                for relation in self._relations
                if query in relation.display_text.lower()
            )
        )

    def all(
        self,
    ) -> SemanticRelationCollection:

        return self._relations

    @property
    def count(
        self,
    ) -> int:

        return len(self._relations)

from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Service

Default application service backed by the canonical
semantic repository.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.semantic.default_semantic_repository import (
    DefaultSemanticRepository,
)

from SanskritAI.domain.semantic.semantic_relation import (
    SemanticRelation,
)

from SanskritAI.domain.semantic.semantic_relation_collection import (
    SemanticRelationCollection,
)

from SanskritAI.domain.semantic.semantic_repository import (
    SemanticRepository,
)

from SanskritAI.domain.semantic.semantic_service import (
    SemanticService,
)


@dataclass(frozen=True, slots=True)
class DefaultSemanticService(
    SemanticService,
):
    """
    Default semantic service.
    """

    _repository: SemanticRepository = field(
        default_factory=DefaultSemanticRepository,
    )

    @property
    def display_name(self) -> str:
        return "Default Semantic Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Application service providing canonical semantic knowledge."
        )

    @property
    def repository(
        self,
    ) -> SemanticRepository:
        return self._repository

    def get_relation(
        self,
        identifier: str,
    ) -> SemanticRelation | None:

        return self.repository.get(identifier)

    def search_relations(
        self,
        query: str,
    ) -> SemanticRelationCollection:

        return self.repository.search(query)

    def all_relations(
        self,
    ) -> SemanticRelationCollection:

        return self.repository.all()

    @property
    def relation_count(
        self,
    ) -> int:

        return self.repository.count

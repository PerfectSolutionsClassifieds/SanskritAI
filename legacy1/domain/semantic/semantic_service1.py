from __future__ import annotations

"""
SanskritAI
==========

Semantic Service

Application service for canonical semantic knowledge.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.semantic.semantic_relation import (
    SemanticRelation,
)

from SanskritAI.domain.semantic.semantic_relation_collection import (
    SemanticRelationCollection,
)

from SanskritAI.domain.semantic.semantic_repository import (
    SemanticRepository,
)


class SemanticService(
    ABC,
    Displayable,
):
    """
    Service abstraction for semantic knowledge.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Application service for canonical semantic knowledge."
        )

    @property
    @abstractmethod
    def repository(
        self,
    ) -> SemanticRepository:
        raise NotImplementedError

    @abstractmethod
    def get_relation(
        self,
        identifier: str,
    ) -> SemanticRelation | None:
        raise NotImplementedError

    @abstractmethod
    def search_relations(
        self,
        query: str,
    ) -> SemanticRelationCollection:
        raise NotImplementedError

    @abstractmethod
    def all_relations(
        self,
    ) -> SemanticRelationCollection:
        raise NotImplementedError

    @property
    @abstractmethod
    def relation_count(
        self,
    ) -> int:
        raise NotImplementedError

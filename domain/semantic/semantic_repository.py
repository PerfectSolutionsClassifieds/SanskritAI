from __future__ import annotations

"""
SanskritAI
==========

Semantic Repository

Repository abstraction for canonical semantic knowledge.

Responsibilities
----------------

• semantic relations

• semantic concepts

• synonym groups

• ontology nodes

• semantic lookup

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.semantic.semantic_relation import SemanticRelation
from SanskritAI.domain.semantic.semantic_relation_collection import (
    SemanticRelationCollection,
)


class SemanticRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for semantic knowledge.
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
            "Abstract repository for canonical semantic knowledge."
        )

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> SemanticRelation | None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> SemanticRelationCollection:
        raise NotImplementedError

    @abstractmethod
    def all(
        self,
    ) -> SemanticRelationCollection:
        raise NotImplementedError

    @property
    @abstractmethod
    def count(
        self,
    ) -> int:
        raise NotImplementedError

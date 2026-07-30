from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Strategy

Defines the abstract strategy for building knowledge graphs.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)


class KnowledgeGraphStrategy(
    ABC,
    Displayable,
):
    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract knowledge graph strategy."

    @abstractmethod
    def analyze(self, context: KnowledgeGraphContext) -> KnowledgeGraphResult:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

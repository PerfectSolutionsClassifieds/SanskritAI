from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Resolver

Defines the façade for knowledge graph construction.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_strategy import (
    KnowledgeGraphStrategy,
)


class KnowledgeGraphResolver(
    Displayable,
):
    def __init__(self, strategy: KnowledgeGraphStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates knowledge graph construction to a strategy."

    @property
    def strategy(self) -> KnowledgeGraphStrategy:
        return self._strategy

    def analyze(self, context: KnowledgeGraphContext) -> KnowledgeGraphResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Default Knowledge Graph Resolver

Thin façade over the default knowledge graph strategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.knowledge_graph.default_knowledge_graph_strategy import (
    DefaultKnowledgeGraphStrategy,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_resolver import (
    KnowledgeGraphResolver,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_strategy import (
    KnowledgeGraphStrategy,
)


class DefaultKnowledgeGraphResolver(
    KnowledgeGraphResolver,
):
    def __init__(
        self,
        strategy: KnowledgeGraphStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultKnowledgeGraphStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Knowledge Graph Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Thin knowledge graph resolver over the default strategy."

    def analyze(self, context: KnowledgeGraphContext) -> KnowledgeGraphResult:
        return self.strategy.analyze(context)

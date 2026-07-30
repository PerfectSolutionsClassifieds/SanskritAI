from __future__ import annotations

"""
SanskritAI
==========

Default Knowledge Graph Strategy

Canonical strategy that ingests semantic, chandas, alankara,
vakya, and derivation outputs into a unified KnowledgeGraph.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.alankara.alankara_analysis_collection import (
    AlankaraAnalysisCollection,
)
from SanskritAI.domain.chandas.chandas_analysis_collection import (
    ChandasAnalysisCollection,
)
from SanskritAI.domain.derivation.derivation_output_collection import (
    DerivationOutputCollection,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph import KnowledgeGraph
from SanskritAI.domain.knowledge_graph.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_diagnostic import (
    KnowledgeGraphDiagnostic,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_strategy import (
    KnowledgeGraphStrategy,
)
from SanskritAI.domain.semantic.semantic_analysis_collection import (
    SemanticAnalysisCollection,
)
from SanskritAI.domain.semantic.semantic_graph import SemanticGraph


class DefaultKnowledgeGraphStrategy(
    KnowledgeGraphStrategy,
):
    def __init__(
        self,
        builder: KnowledgeGraphBuilder | None = None,
    ) -> None:
        self._builder = builder if builder is not None else KnowledgeGraphBuilder()

    @property
    def builder(self) -> KnowledgeGraphBuilder:
        return self._builder

    @property
    def display_name(self) -> str:
        return "Default Knowledge Graph Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical knowledge graph strategy."

    def _merge_source_graphs(
        self,
        context: KnowledgeGraphContext,
    ) -> KnowledgeGraph:
        graph = KnowledgeGraph(
            identifier=context.identifier,
            label="Knowledge Graph",
            description="Unified graph built from upstream kernel outputs.",
            metadata=dict(context.metadata),
        )

        semantic = context.get("semantic")
        if isinstance(semantic, SemanticGraph):
            graph = graph.merge(self.builder.from_semantic(context.identifier, semantic))
        elif isinstance(semantic, SemanticAnalysisCollection):
            graph = graph.merge(self.builder.from_semantic(context.identifier, semantic))

        chandas = context.get("chandas")
        if isinstance(chandas, ChandasAnalysisCollection):
            graph = graph.merge(self.builder.from_chandas(context.identifier, chandas))

        alankara = context.get("alankara")
        if isinstance(alankara, AlankaraAnalysisCollection):
            graph = graph.merge(self.builder.from_alankara(context.identifier, alankara))

        derivation = context.get("derivation")
        if isinstance(derivation, DerivationOutputCollection):
            graph = graph.merge(self.builder.from_derivation(context.identifier, derivation))

        vakya = context.get("vakya")
        if vakya is not None:
            graph = graph.add_node(
                self.builder._node(
                    identifier=f"{context.identifier}:vakya",
                    label="Vakya",
                    node_type="vakya",
                    description=str(getattr(vakya, "display_description", "")),
                    payload={"value": str(getattr(vakya, "display_text", vakya))},
                    confidence=float(getattr(vakya, "confidence", 0.90)),
                )
            )

        return graph

    def analyze(
        self,
        context: KnowledgeGraphContext,
    ) -> KnowledgeGraphResult:
        graph = self._merge_source_graphs(context)

        if graph.is_empty:
            return KnowledgeGraphResult(
                context=context,
                graph=KnowledgeGraph(identifier=context.identifier),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    KnowledgeGraphDiagnostic(
                        code="KG_NO_GRAPH",
                        message="No knowledge graph could be constructed.",
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if graph.node_count > 0 else 0.0

        return KnowledgeGraphResult(
            context=context,
            graph=graph,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )

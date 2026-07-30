from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Builder

Builds KnowledgeGraph objects from upstream kernel outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any

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
from SanskritAI.domain.knowledge_graph.knowledge_graph_edge import (
    KnowledgeGraphEdge,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
    KnowledgeGraphNode,
)
from SanskritAI.domain.semantic.semantic_analysis_collection import (
    SemanticAnalysisCollection,
)
from SanskritAI.domain.semantic.semantic_concept import SemanticConcept
from SanskritAI.domain.semantic.semantic_frame import SemanticFrame
from SanskritAI.domain.semantic.semantic_graph import SemanticGraph


@dataclass(frozen=True, slots=True)
class KnowledgeGraphBuilder(
    Displayable,
):
    @property
    def display_name(self) -> str:
        return "Knowledge Graph Builder"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Builds KnowledgeGraph instances from upstream outputs."

    def _node(
        self,
        identifier: str,
        label: str,
        node_type: str,
        description: str,
        payload: dict[str, Any],
        confidence: float = 1.0,
    ) -> KnowledgeGraphNode:
        return KnowledgeGraphNode(
            identifier=identifier,
            label=label,
            node_type=node_type,
            description=description,
            payload=payload,
            confidence=confidence,
        )

    def from_semantic(
        self,
        identifier: str,
        semantic: SemanticGraph | SemanticAnalysisCollection,
    ) -> KnowledgeGraph:
        graph = KnowledgeGraph(
            identifier=identifier,
            label="Knowledge Graph",
            description="Semantic-derived knowledge graph.",
            metadata={"source": "semantic"},
        )

        if isinstance(semantic, SemanticGraph):
            for concept in semantic.concepts:
                graph = graph.add_node(
                    self._node(
                        identifier=concept.identifier,
                        label=concept.display_text,
                        node_type="semantic.concept",
                        description=concept.description,
                        payload={
                            "gloss": concept.gloss,
                            "category": concept.category,
                        },
                    )
                )
            for relation in semantic.relations:
                source = self._node(
                    identifier=relation.source.identifier,
                    label=relation.source.display_text,
                    node_type="semantic.concept",
                    description=relation.source.description,
                    payload={"gloss": relation.source.gloss},
                )
                target = self._node(
                    identifier=relation.target.identifier,
                    label=relation.target.display_text,
                    node_type="semantic.concept",
                    description=relation.target.description,
                    payload={"gloss": relation.target.gloss},
                )
                graph = graph.add_edge(
                    KnowledgeGraphEdge(
                        identifier=relation.identifier,
                        relation=relation.relation,
                        source=source,
                        target=target,
                        confidence=relation.confidence,
                        description=relation.notes,
                    )
                )
            return graph

        for index, analysis in enumerate(semantic, start=1):
            concept = self._node(
                identifier=f"{identifier}:semantic:{index}",
                label=analysis.display_name,
                node_type="semantic.analysis",
                description=analysis.display_description,
                payload={
                    "text": analysis.text,
                    "meaning": analysis.meaning,
                    "semantic_type": analysis.semantic_type,
                },
                confidence=analysis.confidence,
            )
            graph = graph.add_node(concept)

        return graph

    def from_chandas(
        self,
        identifier: str,
        chandas: ChandasAnalysisCollection,
    ) -> KnowledgeGraph:
        graph = KnowledgeGraph(
            identifier=identifier,
            label="Knowledge Graph",
            description="Chandas-derived knowledge graph.",
            metadata={"source": "chandas"},
        )

        for index, analysis in enumerate(chandas, start=1):
            graph = graph.add_node(
                self._node(
                    identifier=f"{identifier}:chandas:{index}",
                    label=analysis.meter or "Chandas",
                    node_type="chandas.analysis",
                    description=analysis.display_description,
                    payload={
                        "text": analysis.text,
                        "meter": analysis.meter,
                        "meter_class": analysis.meter_class,
                        "syllable_count": analysis.syllable_count,
                        "pada_count": analysis.pada_count,
                    },
                    confidence=analysis.confidence,
                )
            )
        return graph

    def from_alankara(
        self,
        identifier: str,
        alankara: AlankaraAnalysisCollection,
    ) -> KnowledgeGraph:
        graph = KnowledgeGraph(
            identifier=identifier,
            label="Knowledge Graph",
            description="Alankara-derived knowledge graph.",
            metadata={"source": "alankara"},
        )

        for index, analysis in enumerate(alankara, start=1):
            graph = graph.add_node(
                self._node(
                    identifier=f"{identifier}:alankara:{index}",
                    label=analysis.alankara or "Alankara",
                    node_type="alankara.analysis",
                    description=analysis.display_description,
                    payload={
                        "text": analysis.text,
                        "alankara": analysis.alankara,
                        "alankara_class": analysis.alankara_class,
                    },
                    confidence=analysis.confidence,
                )
            )
        return graph

    def from_derivation(
        self,
        identifier: str,
        derivation: DerivationOutputCollection,
    ) -> KnowledgeGraph:
        graph = KnowledgeGraph(
            identifier=identifier,
            label="Knowledge Graph",
            description="Derivation-derived knowledge graph.",
            metadata={"source": "derivation"},
        )

        for index, output in enumerate(derivation, start=1):
            node = self._node(
                identifier=f"{identifier}:derivation:{index}",
                label=output.surface_form,
                node_type="derivation.output",
                description=output.display_description,
                payload={
                    "pada": output.pada,
                    "source_pattern": output.source_pattern,
                    "matched_rule": output.matched_rule,
                    "dhatu": output.dhatu.root,
                    "pratyaya": output.pratyaya.pratyaya,
                },
                confidence=output.confidence,
            )
            graph = graph.add_node(node)
        return graph

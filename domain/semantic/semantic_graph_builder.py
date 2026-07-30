from __future__ import annotations

"""
SanskritAI
==========

Semantic Graph Builder

Builds SemanticGraph objects from semantic analyses, frames,
and upstream kernel outputs.

This builder gives the Semantic Kernel a convenient way to
produce a structured meaning graph alongside the
SemanticAnalysisCollection.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.semantic.semantic_analysis import SemanticAnalysis
from SanskritAI.domain.semantic.semantic_analysis_collection import (
    SemanticAnalysisCollection,
)
from SanskritAI.domain.semantic.semantic_concept import SemanticConcept
from SanskritAI.domain.semantic.semantic_frame import SemanticFrame
from SanskritAI.domain.semantic.semantic_frame_builder import (
    SemanticFrameBuilder,
)
from SanskritAI.domain.semantic.semantic_graph import SemanticGraph
from SanskritAI.domain.semantic.semantic_relation import SemanticRelation


@dataclass(frozen=True, slots=True)
class SemanticGraphBuilder(
    Displayable,
):
    """
    Builds immutable semantic graphs from semantic analysis
    artifacts.
    """

    frame_builder: SemanticFrameBuilder = field(
        default_factory=SemanticFrameBuilder
    )

    @property
    def display_name(self) -> str:
        return "Semantic Graph Builder"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Builds SemanticGraph instances from semantic inputs."

    def _ensure_concept(
        self,
        graph: SemanticGraph,
        concept: SemanticConcept,
    ) -> SemanticGraph:
        return graph.add_concept(concept)

    def _ensure_relation(
        self,
        graph: SemanticGraph,
        relation: SemanticRelation,
    ) -> SemanticGraph:
        return graph.add_relation(relation)

    def _ensure_frame(
        self,
        graph: SemanticGraph,
        frame: SemanticFrame,
    ) -> SemanticGraph:
        return graph.add_frame(frame)

    def from_analysis(
        self,
        identifier: str,
        analyses: SemanticAnalysisCollection | Iterable[SemanticAnalysis],
        *,
        label: str = "",
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> SemanticGraph:
        """
        Builds a semantic graph from one or more semantic analyses.
        """
        if isinstance(analyses, SemanticAnalysisCollection):
            normalized_analyses = analyses
        else:
            normalized_analyses = SemanticAnalysisCollection(
                analyses=tuple(analyses)
            )

        graph = SemanticGraph(
            identifier=identifier,
            label=label or "Semantic Graph",
            description=description,
            metadata=dict(metadata or {}),
        )

        for index, analysis in enumerate(normalized_analyses, start=1):
            concept = SemanticConcept(
                identifier=f"{identifier}:concept:{index}",
                name=analysis.semantic_type or "Meaning",
                gloss=analysis.meaning or analysis.text,
                category="analysis",
                description=analysis.notes,
            )
            graph = self._ensure_concept(graph, concept)

            relation_target = SemanticConcept(
                identifier=f"{identifier}:concept:{index}:target",
                name="Meaning",
                gloss=analysis.meaning or analysis.text,
                category="meaning",
                description=analysis.notes,
            )
            graph = self._ensure_concept(graph, relation_target)

            relation = SemanticRelation(
                identifier=f"{identifier}:relation:{index}",
                relation=analysis.matched_rule or "describes",
                source=concept,
                target=relation_target,
                confidence=analysis.confidence,
                notes=analysis.notes,
            )
            graph = self._ensure_relation(graph, relation)

        return graph

    def from_upstream(
        self,
        identifier: str,
        upstream: Any,
        *,
        label: str = "",
        role: str = "",
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> SemanticGraph:
        """
        Builds a semantic graph from an upstream kernel output.
        """
        frame = self.frame_builder.from_upstream(
            identifier=identifier,
            label=label or "Semantic Frame",
            upstream=upstream,
            role=role,
            confidence=float(
                getattr(upstream, "confidence", 0.90)
            ),
            notes=description,
        )

        graph = SemanticGraph(
            identifier=identifier,
            label=label or frame.label,
            description=description or frame.display_description,
            metadata=dict(metadata or {}),
        )

        graph = self._ensure_frame(graph, frame)
        return graph

    def from_vakya(
        self,
        identifier: str,
        vakya: Any,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> SemanticGraph:
        """
        Builds a semantic graph from Vakya output.
        """
        return self.from_upstream(
            identifier=identifier,
            upstream=vakya,
            label="Vakya Semantic Graph",
            role="sentence",
            description="Graph built from Vakya output.",
            metadata=metadata,
        )

    def from_derivation(
        self,
        identifier: str,
        derivation: Any,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> SemanticGraph:
        """
        Builds a semantic graph from Derivation output.
        """
        return self.from_upstream(
            identifier=identifier,
            upstream=derivation,
            label="Derivation Semantic Graph",
            role="derives-from",
            description="Graph built from Derivation output.",
            metadata=metadata,
        )

    def from_samasa(
        self,
        identifier: str,
        samasa: Any,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> SemanticGraph:
        """
        Builds a semantic graph from Samasa output.
        """
        return self.from_upstream(
            identifier=identifier,
            upstream=samasa,
            label="Samasa Semantic Graph",
            role="compound",
            description="Graph built from Samasa output.",
            metadata=metadata,
        )

    def from_grammar(
        self,
        identifier: str,
        grammar: Any,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> SemanticGraph:
        """
        Builds a semantic graph from Grammar output.
        """
        return self.from_upstream(
            identifier=identifier,
            upstream=grammar,
            label="Grammar Semantic Graph",
            role="grammatical",
            description="Graph built from Grammar output.",
            metadata=metadata,
        )

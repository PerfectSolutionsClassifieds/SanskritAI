from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Result

Defines the immutable outcome of KnowledgeGraph construction.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.knowledge_graph.knowledge_graph import KnowledgeGraph
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_diagnostic import (
    KnowledgeGraphDiagnostic,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGraphResult(
    ValueObject,
    Immutable,
    Displayable,
):
    context: KnowledgeGraphContext

    graph: KnowledgeGraph = field(
        default_factory=lambda: KnowledgeGraph(identifier="empty")
    )

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[KnowledgeGraphDiagnostic, ...] = field(default_factory=tuple)

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def display_name(self) -> str:
        return "Knowledge Graph Result"

    @property
    def display_text(self) -> str:
        state = "Succeeded" if self.succeeded else "Failed"
        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:
        if self.has_diagnostics:
            return self.diagnostics[0].message
        if self.has_graph:
            return self.graph.display_text
        return ""

    @property
    def subject(self):
        return self.context.subject

    @property
    def source(self) -> str:
        return self.context.source

    @property
    def language(self) -> str:
        return self.context.language

    @property
    def script(self) -> str:
        return self.context.script

    @property
    def has_graph(self) -> bool:
        return not self.graph.is_empty

    @property
    def node_count(self) -> int:
        return self.graph.node_count

    @property
    def edge_count(self) -> int:
        return self.graph.edge_count

    @property
    def result(self) -> KnowledgeGraph:
        return self.graph

    @property
    def has_diagnostics(self) -> bool:
        return len(self.diagnostics) > 0

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def first_diagnostic(self) -> KnowledgeGraphDiagnostic | None:
        if not self.diagnostics:
            return None
        return self.diagnostics[0]

    @property
    def resolved(self) -> bool:
        return self.succeeded and self.has_graph

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text

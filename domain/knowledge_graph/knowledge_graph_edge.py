from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Edge

Represents one labeled edge between knowledge graph nodes.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
    KnowledgeGraphNode,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGraphEdge(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable knowledge graph edge.
    """

    identifier: str

    relation: str

    source: KnowledgeGraphNode

    target: KnowledgeGraphNode

    confidence: float = 1.0

    description: str = ""

    payload: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return self.relation

    @property
    def display_text(self) -> str:
        return f"{self.source.label} —{self.relation}→ {self.target.label}"

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_payload(self) -> bool:
        return bool(self.payload)

    def __str__(self) -> str:
        return self.display_text

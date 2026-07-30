from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph

Represents the unified graph of meaning, structure, style,
meter, and derivation evidence.

The KnowledgeGraph is intended to ingest outputs from:
    • Semantic
    • Chandas
    • Alankara
    • Vakya
    • Derivation

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.knowledge_graph.knowledge_graph_edge import (
    KnowledgeGraphEdge,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
    KnowledgeGraphNode,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGraph(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable knowledge graph.
    """

    identifier: str

    nodes: tuple[KnowledgeGraphNode, ...] = field(default_factory=tuple)

    edges: tuple[KnowledgeGraphEdge, ...] = field(default_factory=tuple)

    label: str = ""

    description: str = ""

    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return self.label or "Knowledge Graph"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def is_empty(self) -> bool:
        return self.node_count == 0 and self.edge_count == 0

    @property
    def has_nodes(self) -> bool:
        return self.node_count > 0

    @property
    def has_edges(self) -> bool:
        return self.edge_count > 0

    def get_node(self, identifier: str) -> KnowledgeGraphNode | None:
        for node in self.nodes:
            if node.identifier == identifier:
                return node
        return None

    def get_edge(self, identifier: str) -> KnowledgeGraphEdge | None:
        for edge in self.edges:
            if edge.identifier == identifier:
                return edge
        return None

    def add_node(self, node: KnowledgeGraphNode) -> "KnowledgeGraph":
        if self.get_node(node.identifier) is not None:
            return self
        return KnowledgeGraph(
            identifier=self.identifier,
            nodes=self.nodes + (node,),
            edges=self.edges,
            label=self.label,
            description=self.description,
            metadata=dict(self.metadata),
        )

    def add_edge(self, edge: KnowledgeGraphEdge) -> "KnowledgeGraph":
        if self.get_edge(edge.identifier) is not None:
            return self

        nodes = self.nodes
        if self.get_node(edge.source.identifier) is None:
            nodes = nodes + (edge.source,)
        if self.get_node(edge.target.identifier) is None:
            nodes = nodes + (edge.target,)

        return KnowledgeGraph(
            identifier=self.identifier,
            nodes=nodes,
            edges=self.edges + (edge,),
            label=self.label,
            description=self.description,
            metadata=dict(self.metadata),
        )

    def merge(self, other: "KnowledgeGraph") -> "KnowledgeGraph":
        graph = self
        for node in other.nodes:
            graph = graph.add_node(node)
        for edge in other.edges:
            graph = graph.add_edge(edge)

        merged_metadata = dict(graph.metadata)
        merged_metadata.update(other.metadata)

        return KnowledgeGraph(
            identifier=graph.identifier,
            nodes=graph.nodes,
            edges=graph.edges,
            label=graph.label or other.label,
            description=graph.description or other.description,
            metadata=merged_metadata,
        )

    def __iter__(self) -> Iterator[KnowledgeGraphNode]:
        return iter(self.nodes)

    def __len__(self) -> int:
        return len(self.nodes)

    def __getitem__(self, index: int) -> KnowledgeGraphNode:
        return self.nodes[index]

    def __str__(self) -> str:
        return self.display_text

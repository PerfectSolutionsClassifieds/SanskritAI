
from __future__ import annotations

import pytest

from SanskritAI.domain.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_edge import (
    KnowledgeGraphEdge,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
    KnowledgeGraphNode,
)


def node(
    identifier: str,
    label: str,
) -> KnowledgeGraphNode:
    return KnowledgeGraphNode(
        identifier=identifier,
        label=label,
    )


def edge(
    identifier: str,
    relation: str,
    source: KnowledgeGraphNode,
    target: KnowledgeGraphNode,
) -> KnowledgeGraphEdge:
    return KnowledgeGraphEdge(
        identifier=identifier,
        relation=relation,
        source=source,
        target=target,
    )


def test_empty_graph_can_be_created():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert graph.identifier == "graph-1"
    assert graph.nodes == ()
    assert graph.edges == ()


def test_graph_defaults_are_applied():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert graph.label == ""
    assert graph.description == ""
    assert graph.metadata == {}


def test_empty_graph_reports_correct_state():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert graph.node_count == 0
    assert graph.edge_count == 0
    assert graph.is_empty is True
    assert graph.has_nodes is False
    assert graph.has_edges is False


def test_graph_display_name_uses_label():
    graph = KnowledgeGraph(
        identifier="graph-1",
        label="Sanskrit Knowledge Graph",
    )

    assert graph.display_name == "Sanskrit Knowledge Graph"


def test_graph_display_name_has_default():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert graph.display_name == "Knowledge Graph"


def test_graph_display_text_matches_display_name():
    graph = KnowledgeGraph(
        identifier="graph-1",
        label="Sanskrit Knowledge Graph",
    )

    assert graph.display_text == "Sanskrit Knowledge Graph"


def test_graph_display_description_returns_description():
    graph = KnowledgeGraph(
        identifier="graph-1",
        description="Unified Sanskrit semantic graph.",
    )

    assert graph.display_description == "Unified Sanskrit semantic graph."


def test_get_node_returns_matching_node():
    rama = node("n1", "राम")

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama,),
    )

    assert graph.get_node("n1") == rama


def test_get_node_returns_none_when_missing():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert graph.get_node("missing") is None


def test_get_edge_returns_matching_edge():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    relation = edge(
        "e1",
        "related_to",
        rama,
        hari,
    )

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
        edges=(relation,),
    )

    assert graph.get_edge("e1") == relation


def test_get_edge_returns_none_when_missing():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert graph.get_edge("missing") is None


def test_add_node_returns_new_graph():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    rama = node("n1", "राम")

    updated = graph.add_node(rama)

    assert updated is not graph
    assert graph.node_count == 0
    assert updated.node_count == 1
    assert updated.get_node("n1") == rama


def test_add_node_preserves_existing_graph_data():
    graph = KnowledgeGraph(
        identifier="graph-1",
        label="Graph",
        description="Description",
        metadata={"source": "test"},
    )

    rama = node("n1", "राम")

    updated = graph.add_node(rama)

    assert updated.identifier == "graph-1"
    assert updated.label == "Graph"
    assert updated.description == "Description"
    assert updated.metadata == {"source": "test"}


def test_duplicate_node_is_not_added():
    rama = node("n1", "राम")

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama,),
    )

    updated = graph.add_node(rama)

    assert updated is graph
    assert updated.node_count == 1


def test_add_edge_adds_missing_source_and_target_nodes():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    relation = edge(
        "e1",
        "related_to",
        rama,
        hari,
    )

    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    updated = graph.add_edge(relation)

    assert updated.edge_count == 1
    assert updated.node_count == 2
    assert updated.get_node("n1") == rama
    assert updated.get_node("n2") == hari
    assert updated.get_edge("e1") == relation


def test_add_edge_preserves_existing_nodes():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    relation = edge(
        "e1",
        "related_to",
        rama,
        hari,
    )

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
    )

    updated = graph.add_edge(relation)

    assert updated.node_count == 2
    assert updated.edge_count == 1


def test_duplicate_edge_is_not_added():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    relation = edge(
        "e1",
        "related_to",
        rama,
        hari,
    )

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
        edges=(relation,),
    )

    updated = graph.add_edge(relation)

    assert updated is graph
    assert updated.edge_count == 1


def test_graph_is_iterable_over_nodes():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
    )

    assert list(graph) == [rama, hari]


def test_graph_len_returns_node_count():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
    )

    assert len(graph) == 2


def test_graph_supports_index_access():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    graph = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
    )

    assert graph[0] == rama
    assert graph[1] == hari


def test_merge_combines_nodes_and_edges():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")
    krishna = node("n3", "कृष्ण")

    first_edge = edge(
        "e1",
        "related_to",
        rama,
        hari,
    )

    second_edge = edge(
        "e2",
        "related_to",
        hari,
        krishna,
    )

    first = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
        edges=(first_edge,),
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        nodes=(hari, krishna),
        edges=(second_edge,),
    )

    merged = first.merge(second)

    assert merged.node_count == 3
    assert merged.edge_count == 2

    assert merged.get_node("n1") == rama
    assert merged.get_node("n2") == hari
    assert merged.get_node("n3") == krishna

    assert merged.get_edge("e1") == first_edge
    assert merged.get_edge("e2") == second_edge


def test_merge_does_not_duplicate_existing_nodes():
    rama = node("n1", "राम")

    first = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama,),
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        nodes=(rama,),
    )

    merged = first.merge(second)

    assert merged.node_count == 1


def test_merge_does_not_duplicate_existing_edges():
    rama = node("n1", "राम")
    hari = node("n2", "हरि")

    relation = edge(
        "e1",
        "related_to",
        rama,
        hari,
    )

    first = KnowledgeGraph(
        identifier="graph-1",
        nodes=(rama, hari),
        edges=(relation,),
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        nodes=(rama, hari),
        edges=(relation,),
    )

    merged = first.merge(second)

    assert merged.edge_count == 1


def test_merge_metadata_uses_other_graph_values_for_overlapping_keys():
    first = KnowledgeGraph(
        identifier="graph-1",
        metadata={
            "source": "first",
            "shared": "first",
        },
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        metadata={
            "shared": "second",
            "additional": "second",
        },
    )

    merged = first.merge(second)

    assert merged.metadata == {
        "source": "first",
        "shared": "second",
        "additional": "second",
    }


def test_merge_preserves_first_label_when_present():
    first = KnowledgeGraph(
        identifier="graph-1",
        label="First Graph",
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        label="Second Graph",
    )

    merged = first.merge(second)

    assert merged.label == "First Graph"


def test_merge_uses_other_label_when_first_is_empty():
    first = KnowledgeGraph(
        identifier="graph-1",
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        label="Second Graph",
    )

    merged = first.merge(second)

    assert merged.label == "Second Graph"


def test_merge_preserves_first_description_when_present():
    first = KnowledgeGraph(
        identifier="graph-1",
        description="First description",
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        description="Second description",
    )

    merged = first.merge(second)

    assert merged.description == "First description"


def test_merge_uses_other_description_when_first_is_empty():
    first = KnowledgeGraph(
        identifier="graph-1",
    )

    second = KnowledgeGraph(
        identifier="graph-2",
        description="Second description",
    )

    merged = first.merge(second)

    assert merged.description == "Second description"


def test_graph_is_immutable():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    with pytest.raises(AttributeError):
        graph.identifier = "changed"


def test_graph_is_slot_based():
    graph = KnowledgeGraph(
        identifier="graph-1",
    )

    assert not hasattr(graph, "__dict__")

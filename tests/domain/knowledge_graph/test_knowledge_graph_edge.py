
from __future__ import annotations

import pytest

from SanskritAI.domain.knowledge_graph.knowledge_graph_edge import (
    KnowledgeGraphEdge,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
    KnowledgeGraphNode,
)


def make_source():
    return KnowledgeGraphNode(
        identifier="lemma:rama",
        label="राम",
        node_type="lemma",
    )


def make_target():
    return KnowledgeGraphNode(
        identifier="sense:1",
        label="विष्णुः",
        node_type="sense",
    )


def make_edge():
    return KnowledgeGraphEdge(
        identifier="edge:1",
        relation="has_sense",
        source=make_source(),
        target=make_target(),
    )


def test_edge_can_be_created():
    edge = make_edge()

    assert edge.identifier == "edge:1"
    assert edge.relation == "has_sense"
    assert edge.source.label == "राम"
    assert edge.target.label == "विष्णुः"


def test_edge_defaults_are_applied():
    edge = make_edge()

    assert edge.confidence == 1.0
    assert edge.description == ""
    assert edge.payload == {}


def test_edge_accepts_full_metadata():
    payload = {
        "source": "monier_williams",
        "evidence": "dictionary",
    }

    edge = KnowledgeGraphEdge(
        identifier="edge:2",
        relation="derived_from",
        source=make_source(),
        target=make_target(),
        confidence=0.87,
        description="Lexical derivation relationship.",
        payload=payload,
    )

    assert edge.confidence == 0.87
    assert edge.description == "Lexical derivation relationship."
    assert edge.payload == payload


def test_display_name_returns_relation():
    edge = make_edge()

    assert edge.display_name == "has_sense"


def test_display_text_contains_source_relation_and_target():
    edge = make_edge()

    assert edge.display_text == "राम —has_sense→ विष्णुः"


def test_display_description_returns_description():
    edge = KnowledgeGraphEdge(
        identifier="edge:3",
        relation="related_to",
        source=make_source(),
        target=make_target(),
        description="Semantic relationship.",
    )

    assert edge.display_description == "Semantic relationship."


def test_has_payload_is_false_when_payload_is_empty():
    edge = make_edge()

    assert edge.has_payload is False


def test_has_payload_is_true_when_payload_exists():
    edge = KnowledgeGraphEdge(
        identifier="edge:4",
        relation="related_to",
        source=make_source(),
        target=make_target(),
        payload={"confidence_source": "dictionary"},
    )

    assert edge.has_payload is True


def test_string_representation_uses_display_text():
    edge = make_edge()

    assert str(edge) == "राम —has_sense→ विष्णुः"


def test_edges_with_same_values_are_equal():
    first = make_edge()
    second = make_edge()

    assert first == second


def test_edge_is_immutable():
    edge = make_edge()

    with pytest.raises(AttributeError):
        edge.relation = "different_relation"


def test_payload_default_is_not_shared_between_instances():
    first = make_edge()
    second = make_edge()

    assert first.payload is not second.payload


def test_edge_is_slot_based():
    edge = make_edge()

    assert not hasattr(edge, "__dict__")


from __future__ import annotations

import pytest

from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
    KnowledgeGraphNode,
)


def test_node_can_be_created_with_required_fields():
    node = KnowledgeGraphNode(
        identifier="lemma:hari",
        label="हरि",
    )

    assert node.identifier == "lemma:hari"
    assert node.label == "हरि"


def test_node_defaults_are_applied():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="राम",
    )

    assert node.node_type == ""
    assert node.description == ""
    assert node.payload == {}
    assert node.confidence == 1.0


def test_node_accepts_full_metadata():
    payload = {
        "source": "monier_williams",
        "sense_count": 3,
    }

    node = KnowledgeGraphNode(
        identifier="lemma:rama",
        label="राम",
        node_type="lemma",
        description="A Sanskrit lexical lemma.",
        payload=payload,
        confidence=0.95,
    )

    assert node.identifier == "lemma:rama"
    assert node.label == "राम"
    assert node.node_type == "lemma"
    assert node.description == "A Sanskrit lexical lemma."
    assert node.payload == payload
    assert node.confidence == 0.95


def test_display_name_returns_label():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    assert node.display_name == "हरिः"


def test_display_text_returns_label():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    assert node.display_text == "हरिः"


def test_display_description_returns_description():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
        description="Vishnu",
    )

    assert node.display_description == "Vishnu"


def test_has_payload_is_false_when_payload_is_empty():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    assert node.has_payload is False


def test_has_payload_is_true_when_payload_exists():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
        payload={"source": "MW"},
    )

    assert node.has_payload is True


def test_string_representation_uses_display_text():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    assert str(node) == "हरिः"


def test_nodes_with_same_values_are_equal():
    first = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    second = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    assert first == second


def test_node_is_immutable():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    with pytest.raises(AttributeError):
        node.label = "राम"


def test_payload_default_is_not_shared_between_instances():
    first = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    second = KnowledgeGraphNode(
        identifier="n2",
        label="राम",
    )

    assert first.payload is not second.payload


def test_node_is_slot_based():
    node = KnowledgeGraphNode(
        identifier="n1",
        label="हरिः",
    )

    assert not hasattr(node, "__dict__")

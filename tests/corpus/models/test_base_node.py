
from __future__ import annotations

"""
SanskritAI
==========

BaseNode Unit Tests

Tests the foundational contract of corpus BaseNode.

The tests intentionally focus only on behavior implemented by
BaseNode itself:

- identifier storage
- metadata storage
- id / identifier aliases
- equality
- type-sensitive equality
- hashing
- representation
- generic subclass compatibility

Hierarchy-specific behavior belongs to the corpus navigation
integration tests.

Version
-------
v0.3.0
"""

from dataclasses import dataclass

import pytest

from SanskritAI.corpus.models.base_node import BaseNode


# =============================================================
# Test Metadata
# =============================================================


@dataclass
class NodeMetadata:
    value: str = ""


# =============================================================
# Test Nodes
# =============================================================


class ConcreteNode(BaseNode[str, NodeMetadata]):
    """Concrete test implementation of BaseNode."""

    pass


class OtherConcreteNode(BaseNode[str, NodeMetadata]):
    """Second concrete node used for type-sensitive equality."""

    pass


# =============================================================
# Construction
# =============================================================


def test_base_node_can_be_used_through_concrete_subclass():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="test"),
    )

    assert isinstance(node, BaseNode)


def test_identifier_is_stored():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    assert node.id == "node-1"


def test_identifier_property_is_alias_for_id():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    assert node.identifier == node.id
    assert node.identifier == "node-1"


def test_metadata_is_stored():
    metadata = NodeMetadata(value="metadata")

    node = ConcreteNode(
        identifier="node-1",
        metadata=metadata,
    )

    assert node.metadata is metadata


# =============================================================
# Generic Identifier Support
# =============================================================


def test_base_node_supports_non_string_identifier():
    node = ConcreteNode(
        identifier="123",
        metadata=NodeMetadata(),
    )

    assert node.id == "123"


def test_base_node_preserves_identifier_value():
    identifier = "corpus.document.001"

    node = ConcreteNode(
        identifier=identifier,
        metadata=NodeMetadata(),
    )

    assert node.id == identifier
    assert node.identifier == identifier


# =============================================================
# Equality
# =============================================================


def test_nodes_with_same_type_and_identifier_are_equal():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="A"),
    )

    node_b = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="B"),
    )

    assert node_a == node_b


def test_nodes_with_different_identifiers_are_not_equal():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    node_b = ConcreteNode(
        identifier="node-2",
        metadata=NodeMetadata(),
    )

    assert node_a != node_b


def test_nodes_with_same_identifier_but_different_types_are_not_equal():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    node_b = OtherConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    assert node_a != node_b


def test_node_is_not_equal_to_unrelated_object():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    assert node != "node-1"
    assert node != None


# =============================================================
# Hashing
# =============================================================


def test_nodes_with_same_type_and_identifier_have_same_hash():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="A"),
    )

    node_b = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="B"),
    )

    assert hash(node_a) == hash(node_b)


def test_nodes_with_different_identifiers_have_different_hashes():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    node_b = ConcreteNode(
        identifier="node-2",
        metadata=NodeMetadata(),
    )

    assert hash(node_a) != hash(node_b)


def test_node_can_be_used_as_set_member():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    values = {node}

    assert node in values


def test_equal_nodes_resolve_to_same_set_member():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="A"),
    )

    node_b = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="B"),
    )

    values = {node_a}

    assert node_b in values


# =============================================================
# Representation
# =============================================================


def test_repr_contains_class_name():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    representation = repr(node)

    assert "ConcreteNode" in representation


def test_repr_contains_identifier():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    representation = repr(node)

    assert "node-1" in representation


def test_repr_follows_expected_base_node_format():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    assert repr(node) == "ConcreteNode(id='node-1')"


# =============================================================
# Metadata Independence
# =============================================================


def test_metadata_does_not_participate_in_equality():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="first"),
    )

    node_b = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="second"),
    )

    assert node_a == node_b


def test_metadata_does_not_participate_in_hash():
    node_a = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="first"),
    )

    node_b = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="second"),
    )

    assert hash(node_a) == hash(node_b)


# =============================================================
# Identity Contract
# =============================================================


def test_id_and_identifier_are_consistent():
    node = ConcreteNode(
        identifier="node-42",
        metadata=NodeMetadata(),
    )

    assert node.id == node.identifier


def test_identifier_is_read_only_property():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    with pytest.raises(AttributeError):
        node.identifier = "node-2"


def test_id_is_read_only_property():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(),
    )

    with pytest.raises(AttributeError):
        node.id = "node-2"


# =============================================================
# Contract Summary
# =============================================================


def test_base_node_contract_is_stable():
    node = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="test"),
    )

    equivalent = ConcreteNode(
        identifier="node-1",
        metadata=NodeMetadata(value="other"),
    )

    assert node.id == "node-1"
    assert node.identifier == "node-1"
    assert node.metadata.value == "test"
    assert repr(node) == "ConcreteNode(id='node-1')"
    assert hash(node) == hash(equivalent)

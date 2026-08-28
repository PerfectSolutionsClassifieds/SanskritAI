
from __future__ import annotations

from dataclasses import dataclass

import pytest

from SanskritAI.corpus.builders.node_builder import NodeBuilder
from SanskritAI.corpus.models.base_node import BaseNode


@dataclass
class DummyMetadata:
    title: str = ""
    description: str = ""
    identifier: str = ""
    sequence_number: int | None = None
    parent_identifier: str = ""


class DummyNode(
    BaseNode[str, DummyMetadata],
):
    """
    Minimal BaseNode implementation used to test NodeBuilder.
    """

    def __init__(
        self,
        identifier: str = "node-id",
        metadata: DummyMetadata | None = None,
    ) -> None:
        super().__init__(
            identifier=identifier,
            metadata=metadata or DummyMetadata(),
        )


class DummyNodeBuilder(
    NodeBuilder[
        DummyNode,
        DummyMetadata,
    ]
):
    """
    Concrete NodeBuilder for contract testing.
    """

    def _create_instance(self) -> DummyNode:
        return DummyNode()


# =============================================================
# Construction
# =============================================================


def test_node_builder_creates_node() -> None:
    builder = DummyNodeBuilder()

    assert isinstance(builder.instance(), DummyNode)


def test_node_builder_creates_fresh_node() -> None:
    builder = DummyNodeBuilder()

    assert builder.instance().id == "node-id"
    assert builder.instance().metadata.title == ""


# =============================================================
# Metadata
# =============================================================


def test_with_metadata_replaces_metadata() -> None:
    builder = DummyNodeBuilder()

    metadata = DummyMetadata(
        title="Test Node",
        description="Description",
    )

    result = builder.with_metadata(metadata)

    assert result is builder
    assert builder.instance().metadata is metadata


def test_with_title_sets_title() -> None:
    builder = DummyNodeBuilder()

    result = builder.with_title("Test Title")

    assert result is builder
    assert builder.instance().metadata.title == "Test Title"


def test_with_description_sets_description() -> None:
    builder = DummyNodeBuilder()

    result = builder.with_description("Test Description")

    assert result is builder
    assert builder.instance().metadata.description == "Test Description"


def test_with_identifier_sets_metadata_identifier() -> None:
    builder = DummyNodeBuilder()

    result = builder.with_identifier("canonical-node-001")

    assert result is builder
    assert (
        builder.instance().metadata.identifier
        == "canonical-node-001"
    )


def test_with_identifier_does_not_change_node_id() -> None:
    builder = DummyNodeBuilder()

    original_id = builder.instance().id

    builder.with_identifier("canonical-node-001")

    assert builder.instance().id == original_id
    assert (
        builder.instance().metadata.identifier
        == "canonical-node-001"
    )


def test_with_sequence_number_sets_sequence_number() -> None:
    builder = DummyNodeBuilder()

    result = builder.with_sequence_number(12)

    assert result is builder
    assert builder.instance().metadata.sequence_number == 12


def test_with_sequence_number_accepts_none() -> None:
    builder = DummyNodeBuilder()

    builder.with_sequence_number(None)

    assert builder.instance().metadata.sequence_number is None


def test_with_parent_identifier_sets_parent() -> None:
    builder = DummyNodeBuilder()

    result = builder.with_parent_identifier("parent-001")

    assert result is builder
    assert (
        builder.instance().metadata.parent_identifier
        == "parent-001"
    )


# =============================================================
# Fluent metadata composition
# =============================================================


def test_metadata_methods_are_fluent() -> None:
    builder = (
        DummyNodeBuilder()
        .with_title("Title")
        .with_description("Description")
        .with_identifier("node-001")
        .with_sequence_number(5)
        .with_parent_identifier("parent-001")
    )

    metadata = builder.instance().metadata

    assert metadata.title == "Title"
    assert metadata.description == "Description"
    assert metadata.identifier == "node-001"
    assert metadata.sequence_number == 5
    assert metadata.parent_identifier == "parent-001"


# =============================================================
# Validation
# =============================================================


def test_empty_title_is_invalid() -> None:
    builder = DummyNodeBuilder()

    with pytest.raises(
        ValueError,
        match="Node title cannot be empty",
    ):
        builder.validate()


def test_whitespace_only_title_is_invalid() -> None:
    builder = DummyNodeBuilder()

    builder.with_title("   ")

    with pytest.raises(
        ValueError,
        match="Node title cannot be empty",
    ):
        builder.validate()


def test_non_empty_title_is_valid() -> None:
    builder = DummyNodeBuilder()

    builder.with_title("A valid title")

    assert builder.validate() is None


def test_is_valid_reflects_title_validation() -> None:
    builder = DummyNodeBuilder()

    assert builder.is_valid is False

    builder.with_title("Valid")

    assert builder.is_valid is True


# =============================================================
# Build
# =============================================================


def test_build_valid_node() -> None:
    builder = DummyNodeBuilder()

    builder.with_title("Test Node")

    result = builder.build()

    assert isinstance(result, DummyNode)
    assert result.metadata.title == "Test Node"


def test_build_returns_independent_node() -> None:
    builder = DummyNodeBuilder()

    builder.with_title("Original")

    result = builder.build()

    result.metadata.title = "Changed"

    assert builder.instance().metadata.title == "Original"


# =============================================================
# Reset
# =============================================================


def test_reset_restores_fresh_node() -> None:
    builder = DummyNodeBuilder()

    builder.with_title("Original")
    builder.with_identifier("node-001")

    result = builder.reset()

    assert result is builder
    assert builder.instance().metadata.title == ""
    assert builder.instance().metadata.identifier == ""


# =============================================================
# Existing instance
# =============================================================


def test_from_instance_preserves_node_data() -> None:
    source = DummyNode(
        identifier="source-id",
        metadata=DummyMetadata(
            title="Source",
            description="Source description",
            identifier="canonical-source",
            sequence_number=7,
            parent_identifier="parent-id",
        ),
    )

    builder = DummyNodeBuilder().from_instance(source)

    assert builder.instance().id == "source-id"
    assert builder.instance().metadata.title == "Source"
    assert (
        builder.instance().metadata.description
        == "Source description"
    )
    assert (
        builder.instance().metadata.identifier
        == "canonical-source"
    )
    assert builder.instance().metadata.sequence_number == 7
    assert (
        builder.instance().metadata.parent_identifier
        == "parent-id"
    )


def test_from_instance_is_independent_from_source() -> None:
    source = DummyNode(
        metadata=DummyMetadata(title="Original"),
    )

    builder = DummyNodeBuilder().from_instance(source)

    source.metadata.title = "Changed"

    assert builder.instance().metadata.title == "Original"

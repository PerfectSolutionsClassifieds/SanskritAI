
from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.corpus.builders.child_node_builder import (
    ChildNodeBuilder,
)
from SanskritAI.corpus.models.base_node import BaseNode


@dataclass
class DummyMetadata:
    title: str = ""


class DummyChild(
    BaseNode[str, DummyMetadata],
):
    """
    Minimal child node for ChildNodeBuilder tests.
    """

    def __init__(
        self,
        identifier: str,
        title: str = "",
    ) -> None:
        super().__init__(
            identifier=identifier,
            metadata=DummyMetadata(title=title),
        )


class DummyContainer(
    BaseNode[str, DummyMetadata],
):
    """
    Minimal parent node used to verify the generic child helpers.

    The container deliberately exposes its own add_child()
    operation so that ChildNodeBuilder can be tested independently
    of ContainerNode.
    """

    def __init__(self) -> None:
        super().__init__(
            identifier="parent-id",
            metadata=DummyMetadata(),
        )

        self.children: list[DummyChild] = []

    def add_child(
        self,
        child: DummyChild,
    ) -> None:
        self.children.append(child)


class DummyChildNodeBuilder(
    ChildNodeBuilder[
        DummyContainer,
        DummyMetadata,
        DummyChild,
    ]
):
    """
    Concrete ChildNodeBuilder used only for generic contract tests.
    """

    def _create_instance(self) -> DummyContainer:
        return DummyContainer()

    def add_child(
        self,
        child: DummyChild,
    ) -> "DummyChildNodeBuilder":
        return self._add_child(
            child,
            self._instance.add_child,
        )

    def add_children(
        self,
        children: list[DummyChild],
    ) -> "DummyChildNodeBuilder":
        return self._add_children(
            children,
            self._instance.add_child,
        )


# =============================================================
# Construction
# =============================================================


def test_child_node_builder_creates_parent_instance() -> None:
    builder = DummyChildNodeBuilder()

    assert isinstance(builder.instance(), DummyContainer)
    assert builder.instance().children == []


# =============================================================
# _add_child
# =============================================================


def test_add_child_adds_single_child() -> None:
    builder = DummyChildNodeBuilder()

    child = DummyChild(
        identifier="child-001",
        title="Child One",
    )

    result = builder.add_child(child)

    assert result is builder
    assert builder.instance().children == [child]


def test_add_child_preserves_child_identity() -> None:
    builder = DummyChildNodeBuilder()

    child = DummyChild("child-001")

    builder.add_child(child)

    assert builder.instance().children[0] is child


def test_add_multiple_single_children_preserves_order() -> None:
    builder = DummyChildNodeBuilder()

    first = DummyChild("child-001")
    second = DummyChild("child-002")
    third = DummyChild("child-003")

    builder.add_child(first)
    builder.add_child(second)
    builder.add_child(third)

    assert builder.instance().children == [
        first,
        second,
        third,
    ]


# =============================================================
# _add_children
# =============================================================


def test_add_children_adds_all_children() -> None:
    builder = DummyChildNodeBuilder()

    children = [
        DummyChild("child-001"),
        DummyChild("child-002"),
        DummyChild("child-003"),
    ]

    result = builder.add_children(children)

    assert result is builder
    assert builder.instance().children == children


def test_add_children_preserves_input_order() -> None:
    builder = DummyChildNodeBuilder()

    children = [
        DummyChild("child-003"),
        DummyChild("child-001"),
        DummyChild("child-002"),
    ]

    builder.add_children(children)

    assert builder.instance().children == children


def test_add_children_accepts_empty_iterable() -> None:
    builder = DummyChildNodeBuilder()

    result = builder.add_children([])

    assert result is builder
    assert builder.instance().children == []


def test_add_children_accepts_generator() -> None:
    builder = DummyChildNodeBuilder()

    children = (
        DummyChild(f"child-{index}")
        for index in range(3)
    )

    builder.add_children(children)

    assert [
        child.id
        for child in builder.instance().children
    ] == [
        "child-0",
        "child-1",
        "child-2",
    ]


# =============================================================
# Fluent behavior
# =============================================================


def test_child_operations_are_fluent() -> None:
    first = DummyChild("child-001")
    second = DummyChild("child-002")

    builder = (
        DummyChildNodeBuilder()
        .add_child(first)
        .add_children([second])
    )

    assert builder.instance().children == [
        first,
        second,
    ]


# =============================================================
# Validation inherited from NodeBuilder
# =============================================================


def test_child_node_builder_inherits_node_validation() -> None:
    builder = DummyChildNodeBuilder()

    assert builder.is_valid is False

    builder.with_title("Parent")

    assert builder.is_valid is True


# =============================================================
# Reset
# =============================================================


def test_reset_removes_existing_children() -> None:
    builder = DummyChildNodeBuilder()

    builder.with_title("Parent")
    builder.add_child(
        DummyChild("child-001")
    )

    builder.reset()

    assert builder.instance().children == []
    assert builder.instance().metadata.title == ""


# =============================================================
# Build
# =============================================================


def test_build_returns_independent_parent_with_children() -> None:
    builder = DummyChildNodeBuilder()

    builder.with_title("Parent")

    child = DummyChild("child-001")
    builder.add_child(child)

    result = builder.build()

    assert result is not builder.instance()
    assert result.children == [child]
    assert result.children is not builder.instance().children


def test_build_deep_copies_children() -> None:
    builder = DummyChildNodeBuilder()

    child = DummyChild(
        "child-001",
        title="Original",
    )

    builder.with_title("Parent")
    builder.add_child(child)

    result = builder.build()

    result.children[0].metadata.title = "Changed"

    assert (
        builder.instance().children[0].metadata.title
        == "Original"
    )


# =============================================================
# Existing instance
# =============================================================


def test_from_instance_preserves_children() -> None:
    source = DummyContainer()

    first = DummyChild("child-001")
    second = DummyChild("child-002")

    source.add_child(first)
    source.add_child(second)

    builder = DummyChildNodeBuilder().from_instance(source)

    assert builder.instance().children == [
        first,
        second,
    ]


def test_from_instance_copies_children_independently() -> None:
    source = DummyContainer()

    child = DummyChild(
        "child-001",
        title="Original",
    )

    source.add_child(child)

    builder = DummyChildNodeBuilder().from_instance(source)

    child.metadata.title = "Changed"

    assert (
        builder.instance().children[0].metadata.title
        == "Original"
    )

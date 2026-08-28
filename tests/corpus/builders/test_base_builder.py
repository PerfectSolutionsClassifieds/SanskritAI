
from __future__ import annotations

from dataclasses import dataclass

import pytest

from SanskritAI.corpus.builders.base_builder import BaseBuilder


@dataclass
class DummyObject:
    value: str = ""
    items: list[str] | None = None

    def __post_init__(self) -> None:
        if self.items is None:
            self.items = []


class DummyBuilder(BaseBuilder[DummyObject]):
    """
    Concrete test implementation of BaseBuilder.

    The production BaseBuilder is abstract because subclasses
    must provide _create_instance().
    """

    def _create_instance(self) -> DummyObject:
        return DummyObject()


class ValidatingDummyBuilder(BaseBuilder[DummyObject]):
    """
    Test builder with explicit validation behavior.
    """

    def _create_instance(self) -> DummyObject:
        return DummyObject()

    def validate(self) -> None:
        if not self._instance.value.strip():
            raise ValueError("Value cannot be empty.")


# =============================================================
# Construction
# =============================================================


def test_base_builder_is_abstract() -> None:
    """
    BaseBuilder requires subclasses to implement
    _create_instance().
    """

    with pytest.raises(TypeError):
        BaseBuilder()


def test_concrete_builder_creates_initial_instance() -> None:
    builder = DummyBuilder()

    assert isinstance(builder.instance(), DummyObject)
    assert builder.instance().value == ""
    assert builder.instance().items == []


# =============================================================
# Instance
# =============================================================


def test_instance_returns_current_working_instance() -> None:
    builder = DummyBuilder()

    instance = builder.instance()

    assert instance is builder._instance


# =============================================================
# Reset
# =============================================================


def test_reset_creates_fresh_instance() -> None:
    builder = DummyBuilder()

    original = builder.instance()
    original.value = "original"
    original.items.append("item")

    result = builder.reset()

    assert result is builder
    assert builder.instance() is not original
    assert builder.instance().value == ""
    assert builder.instance().items == []


def test_reset_allows_builder_reuse() -> None:
    builder = DummyBuilder()

    builder.instance().value = "first"

    builder.reset()

    builder.instance().value = "second"

    assert builder.instance().value == "second"


# =============================================================
# Build
# =============================================================


def test_build_returns_constructed_object() -> None:
    builder = DummyBuilder()

    builder.instance().value = "hello"

    result = builder.build()

    assert isinstance(result, DummyObject)
    assert result.value == "hello"


def test_build_returns_deep_copy() -> None:
    builder = DummyBuilder()

    builder.instance().value = "hello"
    builder.instance().items.append("one")

    result = builder.build()

    assert result is not builder.instance()
    assert result.items is not builder.instance().items


def test_build_does_not_disconnect_builder_from_working_instance() -> None:
    builder = DummyBuilder()

    builder.instance().value = "hello"

    result = builder.build()

    result.value = "changed"
    result.items.append("result-only")

    assert builder.instance().value == "hello"
    assert builder.instance().items == []


# =============================================================
# Validation
# =============================================================


def test_default_validate_succeeds() -> None:
    builder = DummyBuilder()

    assert builder.validate() is None


def test_build_calls_validation() -> None:
    builder = ValidatingDummyBuilder()

    with pytest.raises(ValueError, match="Value cannot be empty"):
        builder.build()


def test_validating_builder_builds_valid_instance() -> None:
    builder = ValidatingDummyBuilder()

    builder.instance().value = "valid"

    result = builder.build()

    assert result.value == "valid"


# =============================================================
# is_valid
# =============================================================


def test_is_valid_returns_true_when_validation_succeeds() -> None:
    builder = ValidatingDummyBuilder()

    builder.instance().value = "valid"

    assert builder.is_valid is True


def test_is_valid_returns_false_when_validation_fails() -> None:
    builder = ValidatingDummyBuilder()

    assert builder.is_valid is False


# =============================================================
# from_instance
# =============================================================


def test_from_instance_copies_existing_object() -> None:
    source = DummyObject(
        value="source",
        items=["one", "two"],
    )

    builder = DummyBuilder().from_instance(source)

    assert builder.instance() is not source
    assert builder.instance().value == "source"
    assert builder.instance().items == ["one", "two"]


def test_from_instance_performs_deep_copy() -> None:
    source = DummyObject(
        value="source",
        items=["one"],
    )

    builder = DummyBuilder().from_instance(source)

    source.items.append("source-only")

    assert builder.instance().items == ["one"]


def test_from_instance_returns_builder_for_fluent_use() -> None:
    source = DummyObject(value="source")

    builder = DummyBuilder()

    result = builder.from_instance(source)

    assert result is builder


# =============================================================
# Clone
# =============================================================


def test_clone_returns_same_builder_type() -> None:
    builder = DummyBuilder()

    clone = builder.clone()

    assert type(clone) is type(builder)
    assert clone is not builder


def test_clone_copies_current_instance() -> None:
    builder = DummyBuilder()

    builder.instance().value = "hello"
    builder.instance().items.append("one")

    clone = builder.clone()

    assert clone.instance().value == "hello"
    assert clone.instance().items == ["one"]


def test_clone_performs_deep_copy() -> None:
    builder = DummyBuilder()

    builder.instance().items.append("one")

    clone = builder.clone()

    clone.instance().items.append("clone-only")

    assert builder.instance().items == ["one"]
    assert clone.instance().items == ["one", "clone-only"]


# =============================================================
# Fluent lifecycle
# =============================================================


def test_builder_lifecycle_is_fluent() -> None:
    source = DummyObject(value="source")

    builder = (
        DummyBuilder()
        .from_instance(source)
        .reset()
    )

    assert builder is not None
    assert isinstance(builder, DummyBuilder)
    assert builder.instance().value == ""

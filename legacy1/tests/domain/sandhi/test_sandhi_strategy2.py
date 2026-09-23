
from __future__ import annotations

import pytest

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)
from SanskritAI.domain.sandhi.sandhi_strategy import (
    SandhiStrategy,
)


class TestSandhiStrategy(
    SandhiStrategy,
):
    """Minimal concrete strategy used to test the abstract contract."""

    def __init__(self) -> None:
        self.received_context = None

    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:

        self.received_context = context

        return SandhiResult(
            context=context,
            value="resolved",
        )


def make_context() -> SandhiContext:
    return SandhiContext(
        identifier="test-context",
        subject="रामोऽस्ति",
    )


def test_strategy_is_abstract():
    assert SandhiStrategy.__abstractmethods__ == {
        "resolve",
    }


def test_concrete_strategy_can_be_instantiated():
    strategy = TestSandhiStrategy()

    assert isinstance(
        strategy,
        SandhiStrategy,
    )


def test_display_name_uses_class_name():
    strategy = TestSandhiStrategy()

    assert (
        strategy.display_name
        == "TestSandhiStrategy"
    )


def test_display_text_matches_display_name():
    strategy = TestSandhiStrategy()

    assert (
        strategy.display_text
        == strategy.display_name
    )


def test_display_description_is_defined():
    strategy = TestSandhiStrategy()

    assert (
        strategy.display_description
        == "Abstract Sandhi analysis strategy."
    )


def test_string_representation_uses_display_text():
    strategy = TestSandhiStrategy()

    assert str(strategy) == strategy.display_text


def test_resolve_returns_sandhi_result():
    strategy = TestSandhiStrategy()

    context = make_context()

    result = strategy.resolve(
        context,
    )

    assert isinstance(
        result,
        SandhiResult,
    )


def test_resolve_receives_context():
    strategy = TestSandhiStrategy()

    context = make_context()

    strategy.resolve(
        context,
    )

    assert (
        strategy.received_context
        is context
    )


def test_resolve_preserves_context():
    strategy = TestSandhiStrategy()

    context = make_context()

    result = strategy.resolve(
        context,
    )

    assert result.context is context


def test_resolve_preserves_subject():
    strategy = TestSandhiStrategy()

    context = make_context()

    result = strategy.resolve(
        context,
    )

    assert (
        result.subject
        == "रामोऽस्ति"
    )


def test_resolve_produces_successful_result():
    strategy = TestSandhiStrategy()

    result = strategy.resolve(
        make_context(),
    )

    assert result.succeeded is True
    assert result.resolved is True


def test_resolve_produces_expected_value():
    strategy = TestSandhiStrategy()

    result = strategy.resolve(
        make_context(),
    )

    assert result.value == "resolved"

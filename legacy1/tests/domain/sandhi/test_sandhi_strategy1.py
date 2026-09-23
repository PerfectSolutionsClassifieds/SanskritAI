
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


# ---------------------------------------------------------------------------
# Test implementation
# ---------------------------------------------------------------------------


class TestSandhiStrategy(SandhiStrategy):
    """
    Minimal concrete implementation used only for testing
    the abstract SandhiStrategy contract.
    """

    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:
        return SandhiResult(
            input_text=context.input_text,
        )


# ---------------------------------------------------------------------------
# Construction / abstract contract
# ---------------------------------------------------------------------------


def test_sandhi_strategy_is_abstract():
    assert SandhiStrategy.__abstractmethods__ == {
        "resolve",
    }


def test_sandhi_strategy_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        SandhiStrategy()


def test_concrete_strategy_can_be_instantiated():
    strategy = TestSandhiStrategy()

    assert isinstance(
        strategy,
        SandhiStrategy,
    )


# ---------------------------------------------------------------------------
# Display semantics
# ---------------------------------------------------------------------------


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


def test_display_description_is_canonical():
    strategy = TestSandhiStrategy()

    assert (
        strategy.display_description
        == "Abstract Sandhi analysis strategy."
    )


def test_string_representation_uses_display_text():
    strategy = TestSandhiStrategy()

    assert str(strategy) == strategy.display_text


def test_string_representation_is_class_name():
    strategy = TestSandhiStrategy()

    assert str(strategy) == "TestSandhiStrategy"


# ---------------------------------------------------------------------------
# Resolution contract
# ---------------------------------------------------------------------------


def test_resolve_returns_sandhi_result():
    strategy = TestSandhiStrategy()

    context = SandhiContext(
        input_text="रामोऽस्ति",
    )

    result = strategy.resolve(
        context,
    )

    assert isinstance(
        result,
        SandhiResult,
    )


def test_resolve_receives_context():
    strategy = TestSandhiStrategy()

    context = SandhiContext(
        input_text="रामोऽस्ति",
    )

    result = strategy.resolve(
        context,
    )

    assert result.input_text == "रामोऽस्ति"


# ---------------------------------------------------------------------------
# Displayable contract
# ---------------------------------------------------------------------------


def test_strategy_is_displayable():
    strategy = TestSandhiStrategy()

    assert strategy.is_displayable is True


def test_to_display_string_returns_display_text():
    strategy = TestSandhiStrategy()

    assert (
        strategy.to_display_string()
        == strategy.display_text
    )

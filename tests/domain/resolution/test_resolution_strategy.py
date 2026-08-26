
from __future__ import annotations

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_strategy import (
    ResolutionStrategy,
)


class ConcreteResolutionStrategy(
    ResolutionStrategy,
):
    """
    Minimal concrete implementation used only to
    verify the ResolutionStrategy contract.
    """

    def resolve(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:

        return ResolutionResult(
            context=context,
        )


def make_context(
    subject: str = "देवोऽस्ति",
) -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject=subject,
    )


def test_resolution_strategy_is_abstract():

    assert (
        ResolutionStrategy.__abstractmethods__
        == {"resolve"}
    )


def test_resolution_strategy_cannot_be_instantiated():

    with pytest.raises(TypeError):
        ResolutionStrategy()


def test_concrete_strategy_is_instance_of_contract():

    strategy = ConcreteResolutionStrategy()

    assert isinstance(
        strategy,
        ResolutionStrategy,
    )


def test_strategy_display_name_defaults_to_class_name():

    strategy = ConcreteResolutionStrategy()

    assert (
        strategy.display_name
        == "ConcreteResolutionStrategy"
    )


def test_strategy_display_text_delegates():

    strategy = ConcreteResolutionStrategy()

    assert (
        strategy.display_text
        == strategy.display_name
    )


def test_strategy_display_description_is_canonical():

    strategy = ConcreteResolutionStrategy()

    assert (
        strategy.display_description
        == "Abstract domain resolution strategy."
    )


def test_strategy_is_displayable():

    strategy = ConcreteResolutionStrategy()

    assert strategy.is_displayable is True


def test_strategy_to_display_string():

    strategy = ConcreteResolutionStrategy()

    assert (
        strategy.to_display_string()
        == strategy.display_text
    )


def test_resolve_returns_resolution_result():

    strategy = ConcreteResolutionStrategy()

    context = make_context()

    result = strategy.resolve(
        context,
    )

    assert isinstance(
        result,
        ResolutionResult,
    )


def test_resolve_preserves_context():

    strategy = ConcreteResolutionStrategy()

    context = make_context()

    result = strategy.resolve(
        context,
    )

    assert result.context is context


def test_strategy_is_stateless():

    strategy = ConcreteResolutionStrategy()

    context = make_context()

    first = strategy.resolve(context)
    second = strategy.resolve(context)

    assert first.context is context
    assert second.context is context


def test_string_representation_uses_display_text():

    strategy = ConcreteResolutionStrategy()

    assert str(strategy) == strategy.display_text


from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_strategy import (
    ResolutionStrategy,
)

from SanskritAI.domain.resolution.resolver import (
    Resolver,
)


class RecordingStrategy(
    ResolutionStrategy,
):
    """
    Test double used to verify resolver delegation.
    """

    def __init__(self):
        self.received_context = None
        self.call_count = 0

    def resolve(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:

        self.received_context = context
        self.call_count += 1

        return ResolutionResult(
            context=context,
        )


class ConcreteResolver(
    Resolver,
):
    """
    Minimal concrete resolver used to test the
    abstract façade behavior.
    """

    @property
    def display_name(self) -> str:
        return "Concrete Resolver"


def make_context(
    subject: str = "देवोऽस्ति",
) -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject=subject,
    )


def test_resolver_can_be_constructed():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert resolver is not None


def test_resolver_stores_strategy():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert resolver.strategy is strategy


def test_strategy_is_read_only():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    try:
        resolver._strategy = RecordingStrategy()
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "Resolver strategy must be read-only."
        )


def test_resolver_display_name():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert (
        resolver.display_name
        == "Concrete Resolver"
    )


def test_resolver_display_text():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert (
        resolver.display_text
        == resolver.display_name
    )


def test_resolver_display_description():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert (
        resolver.display_description
        == "Abstract domain resolver."
    )


def test_resolver_is_displayable():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert resolver.is_displayable is True


def test_resolver_to_display_string():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert (
        resolver.to_display_string()
        == resolver.display_text
    )


def test_resolve_delegates_to_strategy():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    context = make_context()

    result = resolver.resolve(
        context,
    )

    assert isinstance(
        result,
        ResolutionResult,
    )


def test_resolve_passes_exact_context_to_strategy():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    context = make_context()

    resolver.resolve(
        context,
    )

    assert (
        strategy.received_context
        is context
    )


def test_resolve_invokes_strategy_exactly_once():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    context = make_context()

    resolver.resolve(
        context,
    )

    assert strategy.call_count == 1


def test_resolve_returns_strategy_result():

    class ReturningStrategy(
        ResolutionStrategy,
    ):

        def resolve(
            self,
            context,
        ):

            return ResolutionResult(
                context=context,
            )

    strategy = ReturningStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    context = make_context()

    result = resolver.resolve(
        context,
    )

    assert result.context is context


def test_resolver_string_representation():

    strategy = RecordingStrategy()

    resolver = ConcreteResolver(
        strategy,
    )

    assert str(resolver) == resolver.display_text

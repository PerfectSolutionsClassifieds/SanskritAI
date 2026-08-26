
from __future__ import annotations

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_resolver import (
    SandhiResolver,
)
from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)
from SanskritAI.domain.sandhi.sandhi_strategy import (
    SandhiStrategy,
)


class ConcreteSandhiStrategy(
    SandhiStrategy,
):
    """Minimal strategy used to test resolver delegation."""

    def __init__(self) -> None:
        self.received_context = None
        self.call_count = 0
        self.result = None

    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:

        self.received_context = context
        self.call_count += 1

        self.result = SandhiResult(
            context=context,
            value="resolved",
        )

        return self.result


def make_context() -> SandhiContext:
    return SandhiContext(
        identifier="context-1",
        subject="रामोऽस्ति",
    )


def make_strategy() -> ConcreteSandhiStrategy:
    return ConcreteSandhiStrategy()


def make_resolver() -> SandhiResolver:
    return SandhiResolver(
        strategy=make_strategy(),
    )


def test_resolver_can_be_instantiated():
    resolver = make_resolver()

    assert isinstance(
        resolver,
        SandhiResolver,
    )


def test_strategy_is_stored():
    strategy = make_strategy()

    resolver = SandhiResolver(
        strategy=strategy,
    )

    assert resolver.strategy is strategy


def test_display_name():
    resolver = make_resolver()

    assert (
        resolver.display_name
        == "SandhiResolver"
    )


def test_display_text_matches_display_name():
    resolver = make_resolver()

    assert (
        resolver.display_text
        == resolver.display_name
    )


def test_display_description():
    resolver = make_resolver()

    assert (
        resolver.display_description
        == "Delegates Sandhi resolution to a strategy."
    )


def test_string_representation():
    resolver = make_resolver()

    assert (
        str(resolver)
        == "SandhiResolver"
    )


def test_resolve_returns_sandhi_result():
    resolver = make_resolver()

    result = resolver.resolve(
        make_context(),
    )

    assert isinstance(
        result,
        SandhiResult,
    )


def test_resolve_delegates_to_strategy():
    strategy = make_strategy()

    resolver = SandhiResolver(
        strategy=strategy,
    )

    context = make_context()

    resolver.resolve(
        context,
    )

    assert strategy.call_count == 1


def test_resolve_passes_context_to_strategy():
    strategy = make_strategy()

    resolver = SandhiResolver(
        strategy=strategy,
    )

    context = make_context()

    resolver.resolve(
        context,
    )

    assert (
        strategy.received_context
        is context
    )


def test_resolve_returns_strategy_result():
    strategy = make_strategy()

    resolver = SandhiResolver(
        strategy=strategy,
    )

    context = make_context()

    result = resolver.resolve(
        context,
    )

    assert (
        result
        is strategy.result
    )


def test_resolve_preserves_context():
    strategy = make_strategy()

    resolver = SandhiResolver(
        strategy=strategy,
    )

    context = make_context()

    result = resolver.resolve(
        context,
    )

    assert (
        result.context
        is context
    )


def test_resolve_can_be_called_multiple_times():
    strategy = make_strategy()

    resolver = SandhiResolver(
        strategy=strategy,
    )

    context1 = make_context()

    context2 = SandhiContext(
        identifier="context-2",
        subject="देवोऽस्ति",
    )

    resolver.resolve(context1)
    resolver.resolve(context2)

    assert strategy.call_count == 2
    assert strategy.received_context is context2

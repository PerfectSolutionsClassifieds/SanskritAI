
from __future__ import annotations

from SanskritAI.domain.sandhi.default_sandhi_resolver import (
    DefaultSandhiResolver,
)

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)


class StubSandhiStrategy:

    def __init__(
        self,
        result,
    ):
        self.result = result
        self.received_context = None

    def resolve(
        self,
        context,
    ):
        self.received_context = context
        return self.result


def make_context():

    return SandhiContext(
        identifier="resolver-test",
        subject="राम + इति",
        source="unit-test",
        language="sa",
        script="Devanagari",
        metadata={},
    )


def test_default_resolver_can_be_constructed():

    resolver = DefaultSandhiResolver()

    assert resolver is not None


def test_default_resolver_uses_default_strategy():

    resolver = DefaultSandhiResolver()

    assert isinstance(
        resolver.strategy,
        DefaultSandhiStrategy,
    )


def test_default_resolver_accepts_explicit_strategy():

    strategy = StubSandhiStrategy(
        object(),
    )

    resolver = DefaultSandhiResolver(
        strategy=strategy,
    )

    assert resolver.strategy is strategy


def test_default_resolver_display_name():

    resolver = DefaultSandhiResolver()

    assert resolver.display_name == (
        "Default Sandhi Resolver"
    )


def test_default_resolver_display_text():

    resolver = DefaultSandhiResolver()

    assert resolver.display_text == (
        resolver.display_name
    )


def test_default_resolver_display_description():

    resolver = DefaultSandhiResolver()

    assert resolver.display_description == (
        "Thin Sandhi resolver façade over the canonical "
        "Sandhi strategy."
    )


def test_default_resolver_delegates_to_strategy():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    resolver = DefaultSandhiResolver(
        strategy=strategy,
    )

    context = make_context()

    result = resolver.resolve(
        context,
    )

    assert result is expected_result
    assert strategy.received_context is context


def test_default_resolver_returns_sandhi_result():

    context = make_context()

    resolver = DefaultSandhiResolver()

    result = resolver.resolve(
        context,
    )

    assert isinstance(
        result,
        SandhiResult,
    )


def test_default_resolver_preserves_context():

    context = make_context()

    resolver = DefaultSandhiResolver()

    result = resolver.resolve(
        context,
    )

    assert result.context is context


def test_default_resolver_string_representation():

    resolver = DefaultSandhiResolver()

    assert str(resolver) == resolver.display_text

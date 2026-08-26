
from __future__ import annotations

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_resolution_kernel import (
    SandhiResolutionKernel,
)


class StubSandhiStrategy:

    def __init__(
        self,
        result=None,
    ):
        self.result = result
        self.received_context = None

    def resolve(
        self,
        context,
    ):
        self.received_context = context
        return self.result


def make_context() -> ResolutionContext:

    return ResolutionContext(
        identifier="test-resolution",
        subject="देव + इन्द्र",
        source="unit-test",
        language="sa",
        script="Devanagari",
        metadata={
            "source_type": "test",
            "recursive": True,
        },
    )


def test_kernel_can_be_constructed_with_strategy():

    strategy = StubSandhiStrategy()

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    assert kernel.strategy is strategy


def test_kernel_uses_default_strategy_when_not_supplied():

    kernel = SandhiResolutionKernel()

    assert isinstance(
        kernel.strategy,
        DefaultSandhiStrategy,
    )


def test_kernel_is_immutable():

    kernel = SandhiResolutionKernel()

    with pytest.raises(
        AttributeError,
    ):
        kernel.strategy = StubSandhiStrategy()


def test_kernel_exposes_resolution_strategy():

    strategy = StubSandhiStrategy()

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    assert kernel.resolution_strategy is strategy


def test_display_name():

    kernel = SandhiResolutionKernel()

    assert (
        kernel.display_name
        == "Sandhi Resolution Kernel"
    )


def test_display_text():

    kernel = SandhiResolutionKernel()

    assert (
        kernel.display_text
        == "Sandhi Resolution Kernel"
    )


def test_display_description():

    kernel = SandhiResolutionKernel()

    assert (
        kernel.display_description
        == (
            "Canonical orchestration layer for the "
            "Sandhi Resolution Kernel."
        )
    )


def test_string_representation():

    kernel = SandhiResolutionKernel()

    assert (
        str(kernel)
        == "Sandhi Resolution Kernel"
    )


def test_build_context_creates_sandhi_context():

    kernel = SandhiResolutionKernel(
        strategy=StubSandhiStrategy(),
    )

    context = make_context()

    sandhi_context = kernel.build_context(
        context,
    )

    assert isinstance(
        sandhi_context,
        SandhiContext,
    )


def test_build_context_preserves_resolution_fields():

    kernel = SandhiResolutionKernel(
        strategy=StubSandhiStrategy(),
    )

    context = make_context()

    sandhi_context = kernel.build_context(
        context,
    )

    assert (
        sandhi_context.identifier
        == context.identifier
    )

    assert (
        sandhi_context.subject
        == context.subject
    )

    assert (
        sandhi_context.source
        == context.source
    )

    assert (
        sandhi_context.language
        == context.language
    )

    assert (
        sandhi_context.script
        == context.script
    )

    assert (
        sandhi_context.metadata
        == context.metadata
    )


def test_resolve_adapts_context_before_strategy_delegation():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    context = make_context()

    result = kernel.resolve(
        context,
    )

    assert result is expected_result

    assert isinstance(
        strategy.received_context,
        SandhiContext,
    )

    assert (
        strategy.received_context.identifier
        == context.identifier
    )

    assert (
        strategy.received_context.subject
        == context.subject
    )


def test_strategy_receives_sandhi_context_not_resolution_context():

    strategy = StubSandhiStrategy(
        object(),
    )

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    kernel.resolve(
        make_context(),
    )

    assert isinstance(
        strategy.received_context,
        SandhiContext,
    )

    assert not isinstance(
        strategy.received_context,
        ResolutionContext,
    )


def test_call_delegates_to_resolve():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    context = make_context()

    result = kernel(
        context,
    )

    assert result is expected_result

    assert isinstance(
        strategy.received_context,
        SandhiContext,
    )


def test_call_and_resolve_produce_same_strategy_result():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    context = make_context()

    assert (
        kernel.resolve(context)
        is expected_result
    )

    assert (
        kernel(context)
        is expected_result
    )

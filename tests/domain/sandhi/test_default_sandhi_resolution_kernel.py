
from __future__ import annotations

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.sandhi.default_sandhi_resolution_kernel import (
    DefaultSandhiResolutionKernel,
)

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)

from SanskritAI.domain.sandhi.sandhi_resolution_kernel import (
    SandhiResolutionKernel,
)


class StubSandhiRepository:
    pass


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


def make_repository():

    return StubSandhiRepository()


def make_context():

    return ResolutionContext(
        identifier="default-kernel-test",
        subject="राम + इति",
        source="unit-test",
        language="sa",
        script="Devanagari",
        metadata={
            "test": True,
        },
    )


def test_default_kernel_can_be_constructed():

    repository = make_repository()

    kernel = DefaultSandhiResolutionKernel(
        repository=repository,
    )

    assert kernel.repository is repository


def test_default_kernel_uses_default_strategy():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    assert isinstance(
        kernel.strategy,
        DefaultSandhiStrategy,
    )


def test_default_kernel_accepts_custom_strategy():

    strategy = StubSandhiStrategy()

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
        strategy=strategy,
    )

    assert kernel.strategy is strategy


def test_default_kernel_is_immutable():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    with pytest.raises(
        AttributeError,
    ):
        kernel.repository = make_repository()


def test_display_name():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    assert (
        kernel.display_name
        == "Default Sandhi Resolution Kernel"
    )


def test_display_text():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    assert (
        kernel.display_text
        == "Default Sandhi Resolution Kernel"
    )


def test_display_description():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    assert (
        kernel.display_description
        == (
            "Default concrete Sandhi Resolution Kernel "
            "composed with a canonical SandhiRepository."
        )
    )


def test_string_representation():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    assert (
        str(kernel)
        == "Default Sandhi Resolution Kernel"
    )


def test_resolution_strategy_returns_configured_strategy():

    strategy = StubSandhiStrategy()

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
        strategy=strategy,
    )

    assert (
        kernel.resolution_strategy
        is strategy
    )


def test_kernel_creates_generic_resolution_kernel():

    strategy = StubSandhiStrategy()

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
        strategy=strategy,
    )

    generic_kernel = kernel.kernel

    assert isinstance(
        generic_kernel,
        SandhiResolutionKernel,
    )

    assert (
        generic_kernel.strategy
        is strategy
    )


def test_kernel_is_recreated_on_each_access():

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
    )

    first = kernel.kernel
    second = kernel.kernel

    assert first is not second

    assert (
        first.strategy
        is kernel.strategy
    )

    assert (
        second.strategy
        is kernel.strategy
    )


def test_resolve_delegates_through_generic_kernel():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
        strategy=strategy,
    )

    context = make_context()

    result = kernel.resolve(
        context,
    )

    assert result is expected_result

    assert strategy.received_context is not None

    assert (
        strategy.received_context.identifier
        == context.identifier
    )

    assert (
        strategy.received_context.subject
        == context.subject
    )


def test_call_delegates_to_resolve():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    kernel = DefaultSandhiResolutionKernel(
        repository=make_repository(),
        strategy=strategy,
    )

    context = make_context()

    result = kernel(
        context,
    )

    assert result is expected_result

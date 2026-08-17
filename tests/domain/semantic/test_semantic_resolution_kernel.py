from __future__ import annotations

from SanskritAI.domain.semantic.semantic_context import (
    SemanticContext,
)

from SanskritAI.domain.semantic.semantic_resolution_kernel import (
    SemanticResolutionKernel,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)

from SanskritAI.domain.semantic.semantic_result import (
    SemanticResult,
)


class StubSemanticStrategy:

    def __init__(self):
        self.received_context = None

    def analyze(
        self,
        context,
    ):
        self.received_context = context

        return SemanticResult(
            context=context,
            value=None,
            succeeded=False,
            confidence=0.0,
            diagnostics=(),
        )


def make_context():

    return SemanticContext(
        identifier="semantic-test",
        subject="धर्मः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
    )


def test_kernel_delegates_to_strategy():

    strategy = StubSemanticStrategy()

    kernel = SemanticResolutionKernel(
        strategy=strategy,
    )

    context = make_context()

    result = kernel.resolve(
        context,
    )

    assert strategy.received_context is context
    assert isinstance(
        result,
        SemanticResolutionResult,
    )


def test_kernel_preserves_context():

    strategy = StubSemanticStrategy()

    kernel = SemanticResolutionKernel(
        strategy=strategy,
    )

    context = make_context()

    result = kernel.resolve(
        context,
    )

    assert result.context is context


def test_kernel_returns_empty_analysis_collection_when_unresolved():

    strategy = StubSemanticStrategy()

    kernel = SemanticResolutionKernel(
        strategy=strategy,
    )

    result = kernel.resolve(
        make_context(),
    )

    assert result.analysis_count == 0
    assert result.succeeded is False

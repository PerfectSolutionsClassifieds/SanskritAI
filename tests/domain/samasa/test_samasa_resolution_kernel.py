
from __future__ import annotations

from SanskritAI.domain.samasa.samasa_context import (
    SamasaContext,
)

from SanskritAI.domain.samasa.samasa_resolution_kernel import (
    SamasaResolutionKernel,
)

from SanskritAI.domain.samasa.samasa_result import (
    SamasaResult,
)

from SanskritAI.domain.samasa.samasa_analysis_collection import (
    SamasaAnalysisCollection,
)


class StubSamasaStrategy:

    def __init__(self):
        self.received_context = None

    def analyze(
        self,
        context,
    ):
        self.received_context = context

        return SamasaResult(
            context=context,
            analyses=SamasaAnalysisCollection(),
            succeeded=False,
            confidence=0.0,
        )


def make_context():

    return SamasaContext(
        identifier="test-samasa",
        subject="राजपुरुषः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
    )


def test_kernel_delegates_to_strategy():

    strategy = StubSamasaStrategy()

    kernel = SamasaResolutionKernel(
        strategy=strategy,
    )

    context = make_context()

    result = kernel.resolve(
        context,
    )

    assert strategy.received_context is context

    assert result is not None

    assert result.context is context


def test_kernel_returns_canonical_resolution_result():

    strategy = StubSamasaStrategy()

    kernel = SamasaResolutionKernel(
        strategy=strategy,
    )

    result = kernel.resolve(
        make_context(),
    )

    from SanskritAI.domain.samasa.samasa_resolution_result import (
        SamasaResolutionResult,
    )

    assert isinstance(
        result,
        SamasaResolutionResult,
    )


def test_kernel_preserves_analysis_collection():

    strategy = StubSamasaStrategy()

    kernel = SamasaResolutionKernel(
        strategy=strategy,
    )

    result = kernel.resolve(
        make_context(),
    )

    assert result.analyses is not None
    assert result.analysis_count == 0

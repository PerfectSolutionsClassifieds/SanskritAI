
from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.sandhi.sandhi_resolution_kernel import (
    SandhiResolutionKernel,
)


class StubSandhiStrategy:

    def __init__(self, result):
        self.result = result
        self.received_context = None

    def resolve(self, context):

        self.received_context = context

        return self.result


def test_kernel_delegates_to_strategy():

    expected_result = object()

    strategy = StubSandhiStrategy(
        expected_result,
    )

    kernel = SandhiResolutionKernel(
        strategy=strategy,
    )

    context = ResolutionContext(
        identifier="test",
        subject="देव + इन्द्र",
        source="unit-test",
        language="sa",
        script="Devanagari",
        metadata={},
    )

    result = kernel.resolve(
        context,
    )

    assert result is expected_result

    assert strategy.received_context is not None

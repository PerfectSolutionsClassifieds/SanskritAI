
from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.sandhi.default_sandhi_resolution_kernel import (
    DefaultSandhiResolutionKernel,
)


class StubSandhiRepository:
    pass


def test_default_kernel_can_be_constructed():

    repository = StubSandhiRepository()

    kernel = DefaultSandhiResolutionKernel(
        repository=repository,
    )

    assert kernel.repository is repository


def test_default_kernel_exposes_resolution_kernel():

    repository = StubSandhiRepository()

    kernel = DefaultSandhiResolutionKernel(
        repository=repository,
    )

    assert kernel.kernel is not None

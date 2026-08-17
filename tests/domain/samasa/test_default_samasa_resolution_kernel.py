
from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.samasa.default_samasa_resolution_kernel import (
    DefaultSamasaResolutionKernel,
)


class StubSamasaRepository:

    count = 0


def make_context():

    return ResolutionContext(
        identifier="test-samasa",
        subject="राजपुरुषः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
        metadata={},
    )


def test_default_kernel_can_be_constructed():

    repository = StubSamasaRepository()

    kernel = DefaultSamasaResolutionKernel(
        repository=repository,
    )

    assert kernel.repository is repository


def test_default_kernel_exposes_generic_kernel():

    repository = StubSamasaRepository()

    kernel = DefaultSamasaResolutionKernel(
        repository=repository,
    )

    assert kernel.kernel is not None


def test_default_kernel_builds_samasa_context():

    repository = StubSamasaRepository()

    kernel = DefaultSamasaResolutionKernel(
        repository=repository,
    )

    context = kernel.build_context(
        make_context(),
    )

    assert context.identifier == "test-samasa"
    assert context.subject == "राजपुरुषः"
    assert context.source == "unit-test"
    assert context.language == "Sanskrit"
    assert context.script == "Devanagari"

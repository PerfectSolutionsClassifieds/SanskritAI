
from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.samasa.samasa_service import (
    SamasaService,
)

from SanskritAI.domain.samasa.default_samasa_resolution_kernel import (
    DefaultSamasaResolutionKernel,
)


class StubSamasaRepository:

    count = 0


def make_context():

    return ResolutionContext(
        identifier="service-test",
        subject="देवालयः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
        metadata={},
    )


def test_service_can_be_constructed():

    repository = StubSamasaRepository()

    service = SamasaService(
        repository=repository,
    )

    assert service.repository is repository


def test_service_creates_default_kernel():

    repository = StubSamasaRepository()

    service = SamasaService(
        repository=repository,
    )

    kernel = service.resolution_kernel

    assert isinstance(
        kernel,
        DefaultSamasaResolutionKernel,
    )

    assert kernel.repository is repository


def test_service_resolve_returns_resolution_result():

    repository = StubSamasaRepository()

    service = SamasaService(
        repository=repository,
    )

    result = service.resolve(
        make_context(),
    )

    from SanskritAI.domain.samasa.samasa_resolution_result import (
        SamasaResolutionResult,
    )

    assert isinstance(
        result,
        SamasaResolutionResult,
    )

from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.semantic.semantic_service import (
    SemanticService,
)

from SanskritAI.domain.semantic.default_semantic_resolution_kernel import (
    DefaultSemanticResolutionKernel,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)


class StubSemanticRepository:

    count = 0


def make_context():

    return ResolutionContext(
        identifier="semantic-service-test",
        subject="मोक्षः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
        metadata={},
    )


def test_service_can_be_constructed():

    repository = StubSemanticRepository()

    service = SemanticService(
        repository=repository,
    )

    assert service.repository is repository


def test_service_creates_default_kernel():

    repository = StubSemanticRepository()

    service = SemanticService(
        repository=repository,
    )

    kernel = service.resolution_kernel

    assert isinstance(
        kernel,
        DefaultSemanticResolutionKernel,
    )

    assert kernel.repository is repository


def test_service_resolve_returns_resolution_result():

    repository = StubSemanticRepository()

    service = SemanticService(
        repository=repository,
    )

    result = service.resolve(
        make_context(),
    )

    assert isinstance(
        result,
        SemanticResolutionResult,
    )

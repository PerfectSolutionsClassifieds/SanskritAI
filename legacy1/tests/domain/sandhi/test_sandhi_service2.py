
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class DummyRepository(SandhiRepository):
    """
    Minimal repository double.

    The service should only retain the repository and pass it
    to the resolution kernel. No repository behavior is tested
    at this boundary.
    """

    def get_rule(self, identifier):
        return None

    def find_by_relation(self, relation):
        return ()

    def all(self):
        return ()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_repository() -> SandhiRepository:
    return DummyRepository()


def make_service() -> SandhiService:
    return SandhiService(
        repository=make_repository(),
    )


def make_context() -> ResolutionContext:
    return ResolutionContext(
        identifier="resolution:1",
        subject="रामोऽस्ति",
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_service_can_be_constructed():
    service = make_service()

    assert isinstance(service, SandhiService)


def test_service_retains_repository():
    repository = make_repository()

    service = SandhiService(
        repository=repository,
    )

    assert service.repository is repository


# ---------------------------------------------------------------------------
# Dataclass / immutability contract
# ---------------------------------------------------------------------------


def test_service_is_immutable():
    service = make_service()

    with pytest.raises(FrozenInstanceError):
        service.repository = make_repository()


def test_service_is_slot_based():
    service = make_service()

    assert not hasattr(service, "__dict__")


# ---------------------------------------------------------------------------
# Display contract
# ---------------------------------------------------------------------------


def test_display_name():
    service = make_service()

    assert service.display_name == "Sandhi Service"


def test_display_text():
    service = make_service()

    assert service.display_text == "Sandhi Service"


def test_display_description():
    service = make_service()

    assert (
        service.display_description
        == "Canonical Sandhi resolution service."
    )


def test_string_representation():
    service = make_service()

    assert str(service) == "Sandhi Service"


# ---------------------------------------------------------------------------
# Kernel composition boundary
# ---------------------------------------------------------------------------


def test_resolution_kernel_is_created_with_repository():
    repository = make_repository()

    service = SandhiService(
        repository=repository,
    )

    kernel = service.resolution_kernel

    assert kernel is not None
    assert kernel.repository is repository


def test_resolution_kernel_is_recreated_from_repository():
    service = make_service()

    first = service.resolution_kernel
    second = service.resolution_kernel

    assert first is not second
    assert first.repository is service.repository
    assert second.repository is service.repository


# ---------------------------------------------------------------------------
# Resolution delegation
# ---------------------------------------------------------------------------


def test_resolve_delegates_to_resolution_kernel(monkeypatch):
    service = make_service()
    context = make_context()

    expected_result = object()
    captured = {}

    class FakeKernel:
        def __init__(self, repository):
            captured["repository"] = repository

        def resolve(self, received_context):
            captured["context"] = received_context
            return expected_result

    monkeypatch.setattr(
        "SanskritAI.domain.sandhi.sandhi_service."
        "DefaultSandhiResolutionKernel",
        FakeKernel,
    )

    result = service.resolve(context)

    assert result is expected_result
    assert captured["repository"] is service.repository
    assert captured["context"] is context


# ---------------------------------------------------------------------------
# ResolutionContributor contract
# ---------------------------------------------------------------------------


def test_contribute_returns_existing_aggregate_unchanged():
    service = make_service()

    aggregate = object()

    result = service.contribute(aggregate)

    assert result is aggregate


def test_contribute_preserves_resolution_result():
    service = make_service()

    aggregate = ResolutionResult(
        identifier="resolution:1",
    )

    result = service.contribute(aggregate)

    assert result is aggregate


# ---------------------------------------------------------------------------
# Type / architectural contracts
# ---------------------------------------------------------------------------


def test_service_is_resolution_contributor():
    service = make_service()

    assert isinstance(
        service,
        ResolutionContributor,
    )


def test_service_has_displayable_contract():
    service = make_service()

    assert service.is_displayable is True

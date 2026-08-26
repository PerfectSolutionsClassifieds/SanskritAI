
from __future__ import annotations

import pytest

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)


# ---------------------------------------------------------------------------
# Test Doubles
# ---------------------------------------------------------------------------


class DummyRepository(SandhiRepository):
    """
    Minimal concrete repository used exclusively for SandhiService tests.

    The implementation deliberately contains no Sandhi logic.
    """

    def get(
        self,
        identifier: str,
    ):
        return None

    def contains(
        self,
        identifier: str,
    ) -> bool:
        return False

    def search(
        self,
        query: str,
    ) -> SandhiRuleSet:
        return SandhiRuleSet()

    def all(
        self,
    ) -> SandhiRuleSet:
        return SandhiRuleSet()

    @property
    def count(
        self,
    ) -> int:
        return 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_repository() -> SandhiRepository:
    return DummyRepository()


def make_service() -> SandhiService:
    return SandhiService(
        repository=make_repository(),
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_service_can_be_constructed():

    service = make_service()

    assert isinstance(
        service,
        SandhiService,
    )


def test_service_retains_repository():

    repository = make_repository()

    service = SandhiService(
        repository=repository,
    )

    assert service.repository is repository


# ---------------------------------------------------------------------------
# Dataclass / Immutability Contract
# ---------------------------------------------------------------------------


def test_service_is_immutable():

    service = make_service()

    with pytest.raises(
        AttributeError,
    ):
        service.repository = make_repository()


def test_service_is_slot_based():

    service = make_service()

    assert not hasattr(
        service,
        "__dict__",
    )


# ---------------------------------------------------------------------------
# Display Contract
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
# Resolution Kernel
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

    first_kernel = service.resolution_kernel
    second_kernel = service.resolution_kernel

    assert first_kernel is not second_kernel
    assert first_kernel.repository is service.repository
    assert second_kernel.repository is service.repository


# ---------------------------------------------------------------------------
# Resolution Delegation
# ---------------------------------------------------------------------------


def test_resolve_delegates_to_resolution_kernel(
    monkeypatch,
):

    service = make_service()

    context = object()
    expected_result = object()

    class StubKernel:

        def resolve(
            self,
            received_context,
        ):

            assert received_context is context

            return expected_result

    monkeypatch.setattr(
        service,
        "resolution_kernel",
        StubKernel(),
    )

    result = service.resolve(
        context,
    )

    assert result is expected_result


# ---------------------------------------------------------------------------
# Resolution Contribution
# ---------------------------------------------------------------------------


def test_contribute_returns_existing_aggregate_unchanged():

    service = make_service()

    aggregate = object()

    result = service.contribute(
        aggregate,
    )

    assert result is aggregate


def test_contribute_preserves_resolution_result():

    service = make_service()

    aggregate = ResolutionResult()

    result = service.contribute(
        aggregate,
    )

    assert result is aggregate


# ---------------------------------------------------------------------------
# Architectural Contracts
# ---------------------------------------------------------------------------


def test_service_is_resolution_contributor():

    service = make_service()

    assert isinstance(
        service,
        ResolutionContributor,
    )


def test_service_has_displayable_contract():

    service = make_service()

    assert hasattr(
        service,
        "display_name",
    )

    assert hasattr(
        service,
        "display_text",
    )

    assert hasattr(
        service,
        "display_description",
    )

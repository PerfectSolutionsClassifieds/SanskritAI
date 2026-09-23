
from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)


# ---------------------------------------------------------------------
# Test Repository
# ---------------------------------------------------------------------


class DummyRepository(SandhiRepository):
    """
    Minimal concrete repository used only for SandhiService tests.

    SandhiService requires a SandhiRepository dependency, but these
    tests do not exercise repository behaviour.
    """

    def __init__(self):
        self._rules: list[SandhiRule] = []

    def get(self, identifier: str):
        for rule in self._rules:
            if rule.identifier == identifier:
                return rule
        return None

    def contains(self, identifier: str) -> bool:
        return self.get(identifier) is not None

    def search(self, query: str):
        return tuple(
            rule
            for rule in self._rules
            if query.lower() in rule.identifier.lower()
        )

    def count(self) -> int:
        return len(self._rules)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def make_repository() -> SandhiRepository:
    return DummyRepository()


def make_service() -> SandhiService:
    return SandhiService(
        repository=make_repository(),
    )


# ---------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------


def test_service_can_be_constructed():

    service = make_service()

    assert service is not None


def test_service_retains_repository():

    repository = make_repository()

    service = SandhiService(
        repository=repository,
    )

    assert service.repository is repository


# ---------------------------------------------------------------------
# Immutability / Slots
# ---------------------------------------------------------------------


def test_service_is_immutable():

    service = make_service()

    try:
        service.repository = make_repository()
        raised = False
    except (
        AttributeError,
        TypeError,
    ):
        raised = True

    assert raised


def test_service_is_slot_based():

    service = make_service()

    assert not hasattr(
        service,
        "__dict__",
    )


# ---------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------


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


# ---------------------------------------------------------------------
# Resolution Kernel
# ---------------------------------------------------------------------


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

    kernel1 = service.resolution_kernel
    kernel2 = service.resolution_kernel

    assert kernel1 is not kernel2
    assert kernel1.repository is service.repository
    assert kernel2.repository is service.repository


# ---------------------------------------------------------------------
# Resolution Delegation
# ---------------------------------------------------------------------


def test_resolve_delegates_to_resolution_kernel(
    monkeypatch,
):

    service = make_service()

    context = ResolutionContext(
        identifier="resolution-1",
        subject="रामोऽस्ति",
    )

    expected = object()

    class StubKernel:

        def resolve(self, received_context):

            assert received_context is context

            return expected

    monkeypatch.setattr(
        service.__class__,
        "resolution_kernel",
        property(
            lambda self: StubKernel()
        ),
    )

    result = service.resolve(context)

    assert result is expected


# ---------------------------------------------------------------------
# Resolution Contribution
# ---------------------------------------------------------------------


def test_contribute_returns_existing_aggregate_unchanged():

    service = make_service()

    aggregate = object()

    result = service.contribute(
        aggregate,
    )

    assert result is aggregate


def test_contribute_preserves_resolution_result():

    service = make_service()

    aggregate = ResolutionResult(
        identifier="resolution-1",
    )

    result = service.contribute(
        aggregate,
    )

    assert result is aggregate


# ---------------------------------------------------------------------
# Architectural Contracts
# ---------------------------------------------------------------------


def test_service_is_resolution_contributor():

    service = make_service()

    assert isinstance(
        service,
        ResolutionContributor,
    )


def test_service_has_displayable_contract():

    service = make_service()

    assert service.is_displayable is True

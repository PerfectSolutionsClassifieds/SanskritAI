
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)

from SanskritAI.domain.resolution.sandhi_resolution_stage import (
    SandhiResolutionStage,
)

from SanskritAI.domain.sandhi.sandhi_resolution_result import (
    SandhiResolutionResult,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class RecordingSandhiService(
    SandhiService,
):
    """
    Minimal Sandhi service used only to test the
    SandhiResolutionStage delegation contract.
    """

    __slots__ = ("calls",)

    def __init__(self) -> None:
        self.calls = []

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SandhiResolutionResult:

        self.calls.append(context)

        return SandhiResolutionResult(
            context=context,
        )


class RecordingContributor(
    ResolutionContributor,
):
    """
    Minimal contributor required by the
    ResolutionStage architectural contract.

    The Sandhi resolution stage performs its linguistic
    work through SandhiService, so this contributor is
    intentionally a no-op test double.
    """

    __slots__ = ()

    def contribute(
        self,
        aggregate,
        context: ResolutionContext,
    ):
        return aggregate


# ---------------------------------------------------------------------------
# Fixtures / factories
# ---------------------------------------------------------------------------


def make_context() -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject="देव इन्द्र",
    )


def make_service() -> RecordingSandhiService:

    return RecordingSandhiService()


def make_contributor() -> RecordingContributor:

    return RecordingContributor()


def make_stage() -> tuple[
    SandhiResolutionStage,
    RecordingSandhiService,
    RecordingContributor,
]:

    service = make_service()
    contributor = make_contributor()

    stage = SandhiResolutionStage(
        contributor=contributor,
        service=service,
    )

    return stage, service, contributor


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_stage_can_be_constructed():

    stage, service, contributor = make_stage()

    assert isinstance(
        stage,
        SandhiResolutionStage,
    )

    assert stage.service is service
    assert stage.contributor is contributor


def test_stage_is_resolution_stage():

    stage, _, _ = make_stage()

    assert isinstance(
        stage,
        ResolutionStage,
    )


def test_stage_is_frozen():

    stage, _, _ = make_stage()

    with pytest.raises(
        FrozenInstanceError,
    ):
        stage.service = (
            make_service()
        )


def test_stage_is_slot_based():

    assert SandhiResolutionStage.__slots__


# ---------------------------------------------------------------------------
# Identity / display
# ---------------------------------------------------------------------------


def test_stage_name():

    stage, _, _ = make_stage()

    assert stage.name == "Sandhi"


def test_stage_display_name():

    stage, _, _ = make_stage()

    assert (
        stage.display_name
        == "Sandhi Resolution Stage"
    )


def test_stage_display_text():

    stage, _, _ = make_stage()

    assert (
        stage.display_text
        == stage.display_name
    )


def test_stage_display_description():

    stage, _, _ = make_stage()

    assert (
        stage.display_description
        == (
            "Pipeline stage responsible for canonical "
            "Sandhi resolution."
        )
    )


def test_stage_is_displayable():

    stage, _, _ = make_stage()

    assert stage.is_displayable is True


def test_stage_to_display_string():

    stage, _, _ = make_stage()

    assert (
        stage.to_display_string()
        == stage.display_text
    )


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


def test_execute_delegates_to_service():

    stage, service, _ = make_stage()

    context = make_context()

    result = stage.execute(
        context,
    )

    assert service.calls == [
        context,
    ]

    assert isinstance(
        result,
        SandhiResolutionResult,
    )


def test_execute_returns_exact_service_result():

    context = make_context()

    class ExactService(
        RecordingSandhiService,
    ):

        def resolve(
            self,
            context: ResolutionContext,
        ):

            self.calls.append(context)

            return SandhiResolutionResult(
                context=context,
            )

    service = ExactService()
    contributor = make_contributor()

    stage = SandhiResolutionStage(
        contributor=contributor,
        service=service,
    )

    expected = service.resolve(
        context,
    )

    service.calls.clear()

    actual = stage.execute(
        context,
    )

    assert actual is not None
    assert actual == expected
    assert service.calls == [
        context,
    ]


def test_execute_preserves_context():

    stage, _, _ = make_stage()

    context = make_context()

    result = stage.execute(
        context,
    )

    assert result.context is context


# ---------------------------------------------------------------------------
# Architectural dependency preservation
# ---------------------------------------------------------------------------


def test_contributor_is_preserved():

    stage, _, contributor = make_stage()

    assert stage.contributor is contributor


def test_service_is_preserved():

    stage, service, _ = make_stage()

    assert stage.service is service


def test_stage_string_representation():

    stage, _, _ = make_stage()

    assert str(stage) == stage.display_text

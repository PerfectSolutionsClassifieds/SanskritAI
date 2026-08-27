
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
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


class RecordingSandhiService(
    SandhiService,
):
    """
    Minimal test double for SandhiService.
    """

    def __init__(self):
        self.calls = []

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SandhiResolutionResult:

        self.calls.append(context)

        return SandhiResolutionResult(
            context=context,
        )


def make_context() -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject="देव इन्द्र",
    )


def make_stage():

    service = RecordingSandhiService()

    stage = SandhiResolutionStage(
        service=service,
    )

    return stage, service


def test_stage_can_be_constructed():

    stage, _ = make_stage()

    assert stage is not None


def test_stage_is_resolution_stage():

    stage, _ = make_stage()

    assert isinstance(
        stage,
        ResolutionStage,
    )


def test_stage_is_frozen():

    stage, _ = make_stage()

    with pytest.raises(
        FrozenInstanceError,
    ):
        stage.service = (
            RecordingSandhiService()
        )


def test_stage_is_slot_based():

    assert SandhiResolutionStage.__slots__


def test_stage_name():

    stage, _ = make_stage()

    assert stage.name == "Sandhi"


def test_stage_display_name():

    stage, _ = make_stage()

    assert (
        stage.display_name
        == "Sandhi Resolution Stage"
    )


def test_stage_display_text():

    stage, _ = make_stage()

    assert (
        stage.display_text
        == stage.display_name
    )


def test_stage_display_description():

    stage, _ = make_stage()

    assert (
        stage.display_description
        == (
            "Pipeline stage responsible for canonical "
            "Sandhi resolution."
        )
    )


def test_stage_is_displayable():

    stage, _ = make_stage()

    assert stage.is_displayable is True


def test_stage_to_display_string():

    stage, _ = make_stage()

    assert (
        stage.to_display_string()
        == stage.display_text
    )


def test_execute_delegates_to_service():

    stage, service = make_stage()

    context = make_context()

    result = stage.execute(
        context,
    )

    assert len(service.calls) == 1

    assert (
        service.calls[0]
        is context
    )

    assert isinstance(
        result,
        SandhiResolutionResult,
    )


def test_execute_preserves_context():

    stage, _ = make_stage()

    context = make_context()

    result = stage.execute(
        context,
    )

    assert result.context is context


def test_string_representation_uses_display_text():

    stage, _ = make_stage()

    assert (
        str(stage)
        == stage.display_text
    )

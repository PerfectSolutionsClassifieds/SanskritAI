
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)

from SanskritAI.domain.resolution.samasa_resolution_stage import (
    SamasaResolutionStage,
)

from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)

from SanskritAI.domain.samasa.samasa_service import (
    SamasaService,
)


class RecordingSamasaService(SamasaService):

    def __init__(self):
        self.calls = []

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SamasaResolutionResult:

        self.calls.append(context)

        return SamasaResolutionResult(
            context=context,
        )


def make_context() -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject="राजपुरुषः",
    )


def make_stage():

    service = RecordingSamasaService()

    stage = SamasaResolutionStage(
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
        stage.service = RecordingSamasaService()


def test_stage_is_slot_based():

    assert SamasaResolutionStage.__slots__


def test_stage_name():

    stage, _ = make_stage()

    assert stage.name == "Samasa"


def test_stage_display_name():

    stage, _ = make_stage()

    assert (
        stage.display_name
        == "Samasa Resolution Stage"
    )


def test_stage_display_text():

    stage, _ = make_stage()

    assert stage.display_text == stage.display_name


def test_stage_display_description():

    stage, _ = make_stage()

    assert (
        stage.display_description
        == (
            "Pipeline stage responsible for canonical "
            "Samāsa resolution."
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

    result = stage.execute(context)

    assert len(service.calls) == 1
    assert service.calls[0] is context

    assert isinstance(
        result,
        SamasaResolutionResult,
    )


def test_execute_preserves_context():

    stage, _ = make_stage()
    context = make_context()

    result = stage.execute(context)

    assert result.context is context


def test_string_representation_uses_display_text():

    stage, _ = make_stage()

    assert str(stage) == stage.display_text

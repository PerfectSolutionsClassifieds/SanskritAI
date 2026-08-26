
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)

from SanskritAI.domain.resolution.lexical_resolution_stage import (
    LexicalResolutionStage,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


class RecordingLexicalService(LexicalService):
    """
    Minimal test double for LexicalService.
    """

    def __init__(self):
        self.calls = []

    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:

        self.calls.append(context)

        return LexicalResolutionResult(
            context=context,
        )


def make_context() -> ResolutionContext:
    return ResolutionContext(
        identifier="context-1",
        subject="देवोऽस्ति",
    )


def make_service() -> RecordingLexicalService:
    return RecordingLexicalService()


def make_stage() -> tuple[
    LexicalResolutionStage,
    RecordingLexicalService,
]:
    service = make_service()

    stage = LexicalResolutionStage(
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
        stage.service = make_service()


def test_stage_is_slot_based():

    assert LexicalResolutionStage.__slots__


def test_stage_name():

    stage, _ = make_stage()

    assert stage.name == "Lexical"


def test_stage_display_name():

    stage, _ = make_stage()

    assert (
        stage.display_name
        == "Lexical Resolution Stage"
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
            "lexical resolution."
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
        LexicalResolutionResult,
    )


def test_execute_returns_exact_service_result():

    context = make_context()

    class ExactService(RecordingLexicalService):

        def resolve(self, context):
            self.calls.append(context)

            return LexicalResolutionResult(
                context=context,
            )

    service = ExactService()

    stage = LexicalResolutionStage(
        service=service,
    )

    result = stage.execute(context)

    assert result.context is context


def test_string_representation_uses_display_text():

    stage, _ = make_stage()

    assert str(stage) == stage.display_text

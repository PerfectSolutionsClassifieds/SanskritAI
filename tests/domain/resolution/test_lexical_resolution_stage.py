
from __future__ import annotations

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

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class RecordingLexicalService(LexicalService):
    """
    Minimal lexical service used only for testing the
    LexicalResolutionStage delegation contract.
    """

    __slots__ = ("calls",)

    def __init__(self) -> None:
        self.calls = []

    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:

        self.calls.append(context)

        return LexicalResolutionResult(
            context=context,
        )


class RecordingContributor(
    ResolutionContributor,
):
    """
    Minimal contributor required by the ResolutionStage
    architectural contract.

    The lexical resolution stage currently performs its
    linguistic work through LexicalService, so this
    contributor is intentionally a no-op test double.
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


def make_context(
    subject: str = "देवोऽस्ति",
) -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject=subject,
    )


def make_service() -> RecordingLexicalService:

    return RecordingLexicalService()


def make_contributor() -> RecordingContributor:

    return RecordingContributor()


def make_stage() -> tuple[
    LexicalResolutionStage,
    RecordingLexicalService,
    RecordingContributor,
]:

    service = make_service()
    contributor = make_contributor()

    stage = LexicalResolutionStage(
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
        LexicalResolutionStage,
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
        (AttributeError, TypeError),
    ):
        stage.service = make_service()


# ---------------------------------------------------------------------------
# Identity / display
# ---------------------------------------------------------------------------


def test_stage_name():

    stage, _, _ = make_stage()

    assert stage.name == "Lexical"


def test_stage_display_name():

    stage, _, _ = make_stage()

    assert (
        stage.display_name
        == "Lexical Resolution Stage"
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
            "lexical resolution."
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

    assert result.context == context


def test_execute_returns_exact_service_result():

    context = make_context()

    class ExactService(
        RecordingLexicalService,
    ):

        def resolve(
            self,
            context: ResolutionContext,
        ):

            self.calls.append(context)

            result = LexicalResolutionResult(
                context=context,
            )

            return result

    service = ExactService()
    contributor = make_contributor()

    stage = LexicalResolutionStage(
        contributor=contributor,
        service=service,
    )

    expected = service.resolve(context)

    service.calls.clear()

    actual = stage.execute(
        context,
    )

    assert actual is not None
    assert actual == expected
    assert service.calls == [context]


def test_execute_preserves_context():

    stage, _, _ = make_stage()

    context = make_context(
        subject="रामः गच्छति",
    )

    result = stage.execute(
        context,
    )

    assert result.context == context
    assert result.context.subject == "रामः गच्छति"


# ---------------------------------------------------------------------------
# Immutability / architecture
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

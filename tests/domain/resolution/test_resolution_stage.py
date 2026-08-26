
from __future__ import annotations

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


class RecordingContributor(
    ResolutionContributor,
):
    """
    Test double used to verify exact delegation.
    """

    def __init__(self):
        self.received_aggregate = None
        self.received_context = None

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:

        self.received_aggregate = aggregate
        self.received_context = context

        return aggregate


def make_context(
    subject: str = "देवोऽस्ति",
) -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject=subject,
    )


def make_result() -> ResolutionResult:

    return ResolutionResult(
        context=make_context(),
    )


def test_resolution_stage_can_be_constructed():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert stage is not None


def test_resolution_stage_stores_contributor():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert stage.contributor is contributor


def test_resolution_stage_is_frozen():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    try:
        stage.contributor = RecordingContributor()
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "ResolutionStage must be immutable."
        )


def test_resolution_stage_is_slot_based():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert not hasattr(
        stage,
        "__dict__",
    )


def test_resolution_stage_display_name_delegates():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert (
        stage.display_name
        == contributor.display_name
    )


def test_resolution_stage_display_text_delegates():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert (
        stage.display_text
        == stage.display_name
    )


def test_resolution_stage_display_description():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert (
        stage.display_description
        == (
            "Pipeline stage using "
            "RecordingContributor."
        )
    )


def test_resolution_stage_context_type():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert (
        stage.context_type
        is ResolutionContext
    )


def test_execute_delegates_to_contributor():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    aggregate = make_result()

    result = stage.execute(
        aggregate,
    )

    assert result is aggregate


def test_execute_passes_same_aggregate():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    aggregate = make_result()

    stage.execute(
        aggregate,
    )

    assert (
        contributor.received_aggregate
        is aggregate
    )


def test_execute_passes_aggregate_context():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    aggregate = make_result()

    stage.execute(
        aggregate,
    )

    assert (
        contributor.received_context
        is aggregate.context
    )


def test_execute_returns_contributor_result():

    class ReturningContributor(
        ResolutionContributor,
    ):

        def contribute(
            self,
            aggregate,
            context,
        ):

            return ResolutionResult(
                context=context,
            )

    contributor = ReturningContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    aggregate = make_result()

    result = stage.execute(
        aggregate,
    )

    assert isinstance(
        result,
        ResolutionResult,
    )

    assert result.context is aggregate.context


def test_string_representation_uses_display_text():

    contributor = RecordingContributor()

    stage = ResolutionStage(
        contributor=contributor,
    )

    assert str(stage) == stage.display_text

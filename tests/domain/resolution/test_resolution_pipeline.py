
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class RecordingContributor(
    ResolutionContributor,
):
    """
    Minimal contributor used to verify pipeline ordering,
    aggregate propagation, and execution semantics.
    """

    __slots__ = (
        "label",
        "calls",
    )

    def __init__(
        self,
        label: str,
        calls: list,
    ) -> None:

        self.label = label
        self.calls = calls

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:

        self.calls.append(
            (
                self.label,
                aggregate,
                context,
            )
        )

        return aggregate


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def make_context(
    subject: str = "देवोऽस्ति",
) -> ResolutionContext:

    return ResolutionContext(
        identifier="context-1",
        subject=subject,
    )


def make_stage(
    label: str,
    calls: list,
) -> ResolutionStage:

    contributor = RecordingContributor(
        label=label,
        calls=calls,
    )

    return ResolutionStage(
        contributor=contributor,
    )


def make_pipeline(
    labels: tuple[str, ...] = (
        "Lexical",
        "Morphology",
        "Sandhi",
    ),
):

    calls = []

    stages = tuple(
        make_stage(
            label,
            calls,
        )
        for label in labels
    )

    pipeline = ResolutionPipeline(
        stages=stages,
    )

    return pipeline, calls


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_pipeline_can_be_constructed():

    pipeline, _ = make_pipeline()

    assert isinstance(
        pipeline,
        ResolutionPipeline,
    )


def test_pipeline_is_frozen():

    pipeline, _ = make_pipeline()

    with pytest.raises(
        FrozenInstanceError,
    ):
        pipeline.stages = ()


def test_pipeline_is_slot_based():

    assert ResolutionPipeline.__slots__


def test_pipeline_stages_are_preserved():

    pipeline, _ = make_pipeline()

    assert len(pipeline.stages) == 3

    assert all(
        isinstance(
            stage,
            ResolutionStage,
        )
        for stage in pipeline.stages
    )


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------


def test_display_name():

    pipeline, _ = make_pipeline()

    assert (
        pipeline.display_name
        == "Resolution Pipeline"
    )


def test_display_text():

    pipeline, _ = make_pipeline()

    assert (
        pipeline.display_text
        == pipeline.display_name
    )


def test_display_description():

    pipeline, _ = make_pipeline()

    assert (
        pipeline.display_description
        == (
            "Canonical Sanskrit linguistic resolution "
            "pipeline."
        )
    )


def test_pipeline_is_displayable():

    pipeline, _ = make_pipeline()

    assert pipeline.is_displayable is True


def test_string_representation():

    pipeline, _ = make_pipeline()

    assert str(pipeline) == pipeline.display_text


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------


def test_stage_count():

    pipeline, _ = make_pipeline()

    assert pipeline.stage_count == 3


def test_empty_pipeline():

    pipeline = ResolutionPipeline()

    assert pipeline.stage_count == 0
    assert pipeline.is_empty is True


def test_non_empty_pipeline():

    pipeline, _ = make_pipeline()

    assert pipeline.stage_count == 3
    assert pipeline.is_empty is False


# ---------------------------------------------------------------------------
# Iteration
# ---------------------------------------------------------------------------


def test_pipeline_is_iterable():

    pipeline, _ = make_pipeline()

    stages = tuple(pipeline)

    assert stages == pipeline.stages


def test_pipeline_len():

    pipeline, _ = make_pipeline()

    assert len(pipeline) == pipeline.stage_count


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


def test_execute_returns_resolution_result():

    pipeline, _ = make_pipeline()

    context = make_context()

    result = pipeline.execute(
        context,
    )

    assert isinstance(
        result,
        ResolutionResult,
    )


def test_execute_preserves_context():

    pipeline, _ = make_pipeline()

    context = make_context(
        subject="रामः वनं गच्छति",
    )

    result = pipeline.execute(
        context,
    )

    assert result.context is context
    assert result.context.subject == (
        "रामः वनं गच्छति"
    )


def test_execute_empty_pipeline_returns_initial_result():

    pipeline = ResolutionPipeline()

    context = make_context()

    result = pipeline.execute(
        context,
    )

    assert isinstance(
        result,
        ResolutionResult,
    )

    assert result.context is context


def test_execute_runs_stages_in_order():

    pipeline, calls = make_pipeline(
        labels=(
            "Lexical",
            "Morphology",
            "Sandhi",
        ),
    )

    context = make_context()

    pipeline.execute(
        context,
    )

    assert [
        label
        for label, _, _ in calls
    ] == [
        "Lexical",
        "Morphology",
        "Sandhi",
    ]


def test_execute_passes_context_to_every_stage():

    pipeline, calls = make_pipeline(
        labels=(
            "Lexical",
            "Morphology",
            "Sandhi",
        ),
    )

    context = make_context()

    pipeline.execute(
        context,
    )

    assert all(
        recorded_context is context
        for _, _, recorded_context in calls
    )


def test_execute_passes_same_aggregate_through_stages():

    pipeline, calls = make_pipeline(
        labels=(
            "Lexical",
            "Morphology",
            "Sandhi",
        ),
    )

    context = make_context()

    result = pipeline.execute(
        context,
    )

    aggregates = [
        aggregate
        for _, aggregate, _ in calls
    ]

    assert len(aggregates) == 3

    assert aggregates[0] is aggregates[1]
    assert aggregates[1] is aggregates[2]

    assert aggregates[-1] is result

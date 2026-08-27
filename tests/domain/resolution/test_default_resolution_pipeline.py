
from __future__ import annotations

from types import SimpleNamespace

from SanskritAI.domain.resolution.default_resolution_pipeline import (
    default_resolution_pipeline,
)

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class RecordingContributor(
    ResolutionContributor,
):
    """
    Minimal contributor representing one registered
    linguistic service.
    """

    __slots__ = (
        "label",
        "calls",
    )

    def __init__(
        self,
        label: str,
    ) -> None:

        self.label = label
        self.calls = []

    def contribute(
        self,
        aggregate,
        context,
    ):

        self.calls.append(
            (
                aggregate,
                context,
            )
        )

        return aggregate


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def make_services():

    lexical = RecordingContributor(
        "Lexical",
    )

    morphological = RecordingContributor(
        "Morphology",
    )

    sandhi = RecordingContributor(
        "Sandhi",
    )

    samasa = RecordingContributor(
        "Samasa",
    )

    semantic = RecordingContributor(
        "Semantic",
    )

    services = SimpleNamespace(
        lexical_service=lexical,
        morphological_service=morphological,
        sandhi_service=sandhi,
        samasa_service=samasa,
        semantic_service=semantic,
    )

    return (
        services,
        (
            lexical,
            morphological,
            sandhi,
            samasa,
            semantic,
        ),
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_default_pipeline_returns_resolution_pipeline():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert isinstance(
        pipeline,
        ResolutionPipeline,
    )


def test_default_pipeline_contains_five_stages():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert pipeline.stage_count == 5


def test_default_pipeline_is_not_empty():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert pipeline.is_empty is False


# ---------------------------------------------------------------------------
# Stage structure
# ---------------------------------------------------------------------------


def test_default_pipeline_contains_resolution_stages():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert all(
        isinstance(
            stage,
            ResolutionStage,
        )
        for stage in pipeline
    )


def test_default_pipeline_stage_order():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert [
        stage.contributor
        for stage in pipeline
    ] == [
        services.lexical_service,
        services.morphological_service,
        services.sandhi_service,
        services.samasa_service,
        services.semantic_service,
    ]


def test_lexical_service_is_first_contributor():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert (
        pipeline.stages[0].contributor
        is services.lexical_service
    )


def test_morphological_service_is_second_contributor():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert (
        pipeline.stages[1].contributor
        is services.morphological_service
    )


def test_sandhi_service_is_third_contributor():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert (
        pipeline.stages[2].contributor
        is services.sandhi_service
    )


def test_samasa_service_is_fourth_contributor():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert (
        pipeline.stages[3].contributor
        is services.samasa_service
    )


def test_semantic_service_is_fifth_contributor():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert (
        pipeline.stages[4].contributor
        is services.semantic_service
    )


# ---------------------------------------------------------------------------
# Contributor identity preservation
# ---------------------------------------------------------------------------


def test_default_pipeline_preserves_all_service_instances():

    services, contributors = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    actual_contributors = tuple(
        stage.contributor
        for stage in pipeline
    )

    assert actual_contributors == contributors

    assert all(
        actual is expected
        for actual, expected in zip(
            actual_contributors,
            contributors,
        )
    )


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------


def test_default_pipeline_executes_all_contributors():

    services, contributors = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    from SanskritAI.domain.resolution.resolution_context import (
        ResolutionContext,
    )

    context = ResolutionContext(
        identifier="context-1",
        subject="देवोऽस्ति",
    )

    result = pipeline.execute(
        context,
    )

    assert result.context is context

    for contributor in contributors:
        assert len(
            contributor.calls
        ) == 1


def test_default_pipeline_executes_contributors_in_order():

    services, contributors = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    from SanskritAI.domain.resolution.resolution_context import (
        ResolutionContext,
    )

    context = ResolutionContext(
        identifier="context-1",
        subject="देवोऽस्ति",
    )

    pipeline.execute(
        context,
    )

    # Every contributor receives the same context.
    assert all(
        recorded_context is context
        for contributor in contributors
        for _, recorded_context
        in contributor.calls
    )


def test_default_pipeline_uses_exact_registered_contributors():

    services, contributors = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    for stage, contributor in zip(
        pipeline,
        contributors,
    ):
        assert stage.contributor is contributor


def test_default_pipeline_can_be_iterated():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    stages = tuple(pipeline)

    assert stages == pipeline.stages


def test_default_pipeline_length_matches_stage_count():

    services, _ = make_services()

    pipeline = default_resolution_pipeline(
        services,
    )

    assert len(pipeline) == 5
    assert len(pipeline) == pipeline.stage_count

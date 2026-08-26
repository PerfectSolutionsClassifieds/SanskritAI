
from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)
from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from SanskritAI.domain.resolution.resolution_state import (
    ResolutionState,
)


def make_context():
    return ResolutionContext(
        identifier="ctx-1",
        subject="हरिः",
    )


def make_state():
    return ResolutionState(
        context=make_context(),
    )


def make_diagnostic():
    return ResolutionDiagnostic(
        code="RES001",
        message="Test diagnostic.",
    )


def test_state_can_be_created_with_context():
    state = make_state()

    assert state.context.identifier == "ctx-1"
    assert state.subject == "हरिः"
    assert state.identifier == "ctx-1"


def test_stage_results_default_to_none():
    state = make_state()

    assert state.lexical_result is None
    assert state.morphological_result is None
    assert state.sandhi_result is None
    assert state.samasa_result is None
    assert state.semantic_result is None


def test_pipeline_metadata_defaults():
    state = make_state()

    assert state.payload is None
    assert state.confidence == 1.0
    assert state.metadata == {}
    assert state.diagnostics == []
    assert state.completed_stages == []
    assert state.failed_stage is None


def test_stage_flags_are_false_initially():
    state = make_state()

    assert not state.has_lexical
    assert not state.has_morphology
    assert not state.has_sandhi
    assert not state.has_samasa
    assert not state.has_semantics


def test_stage_count_is_zero_initially():
    state = make_state()

    assert state.stage_count == 0


def test_state_succeeds_initially():
    state = make_state()

    assert not state.has_failures
    assert state.succeeded


def test_state_is_slot_based():
    state = make_state()

    assert not hasattr(state, "__dict__")


def test_state_is_mutable():
    state = make_state()

    state.confidence = 0.75

    assert state.confidence == 0.75


def test_mark_completed_adds_stage():
    state = make_state()

    state.mark_completed("lexical")

    assert state.completed_stages == ["lexical"]
    assert state.stage_count == 1


def test_mark_completed_preserves_stage_order():
    state = make_state()

    state.mark_completed("lexical")
    state.mark_completed("morphology")
    state.mark_completed("sandhi")

    assert state.completed_stages == [
        "lexical",
        "morphology",
        "sandhi",
    ]
    assert state.stage_count == 3


def test_mark_failed_records_failed_stage():
    state = make_state()

    state.mark_failed("morphology")

    assert state.failed_stage == "morphology"
    assert state.has_failures
    assert not state.succeeded


def test_mark_completed_does_not_clear_failure():
    state = make_state()

    state.mark_failed("morphology")
    state.mark_completed("lexical")

    assert state.failed_stage == "morphology"
    assert state.has_failures


def test_add_diagnostic():
    state = make_state()
    diagnostic = make_diagnostic()

    state.add_diagnostic(diagnostic)

    assert state.diagnostics == [diagnostic]


def test_multiple_diagnostics_are_preserved():
    state = make_state()

    first = make_diagnostic()
    second = ResolutionDiagnostic(
        code="RES002",
        message="Second diagnostic.",
    )

    state.add_diagnostic(first)
    state.add_diagnostic(second)

    assert state.diagnostics == [
        first,
        second,
    ]


def test_set_metadata():
    state = make_state()

    state.set_metadata(
        "chapter",
        10,
    )

    assert state.metadata == {
        "chapter": 10,
    }


def test_get_metadata_returns_value():
    state = make_state()

    state.set_metadata(
        "chapter",
        10,
    )

    assert state.get_metadata("chapter") == 10


def test_get_metadata_returns_default():
    state = make_state()

    assert state.get_metadata(
        "missing",
        "default",
    ) == "default"


def test_stage_result_flags_reflect_assigned_results():
    state = make_state()

    state.lexical_result = object()
    state.morphological_result = object()
    state.sandhi_result = object()
    state.samasa_result = object()
    state.semantic_result = object()

    assert state.has_lexical
    assert state.has_morphology
    assert state.has_sandhi
    assert state.has_samasa
    assert state.has_semantics


def test_state_can_accumulate_complete_pipeline_progress():
    state = make_state()

    state.lexical_result = object()
    state.mark_completed("lexical")

    state.morphological_result = object()
    state.mark_completed("morphology")

    state.sandhi_result = object()
    state.mark_completed("sandhi")

    state.samasa_result = object()
    state.mark_completed("samasa")

    state.semantic_result = object()
    state.mark_completed("semantic")

    assert state.stage_count == 5
    assert state.completed_stages == [
        "lexical",
        "morphology",
        "sandhi",
        "samasa",
        "semantic",
    ]
    assert state.succeeded

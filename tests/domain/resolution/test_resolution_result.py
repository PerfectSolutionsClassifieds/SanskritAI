
from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)
from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


def make_context():
    return ResolutionContext(
        identifier="ctx-1",
        subject="हरिः",
    )


def make_result(**overrides):
    values = {
        "context": make_context(),
    }
    values.update(overrides)
    return ResolutionResult(**values)


def make_diagnostic():
    return ResolutionDiagnostic(
        code="RES001",
        message="Diagnostic message.",
    )


def test_result_can_be_created_with_context():
    result = make_result()

    assert result.context.identifier == "ctx-1"
    assert result.subject == "हरिः"


def test_stage_results_default_to_none():
    result = make_result()

    assert result.lexical is None
    assert result.morphology is None
    assert result.sandhi is None
    assert result.samasa is None
    assert result.semantic is None


def test_default_diagnostics_are_empty():
    result = make_result()

    assert result.diagnostics == ()
    assert not result.has_diagnostics
    assert result.diagnostic_count == 0


def test_default_confidence_and_success():
    result = make_result()

    assert result.confidence == 0.0
    assert result.succeeded is True


def test_display_properties():
    result = make_result()

    assert result.display_name == "Resolution Result"
    assert result.display_text == "Resolution Result"
    assert (
        result.display_description
        == "Aggregate linguistic resolution."
    )


def test_stage_presence_flags_are_false_initially():
    result = make_result()

    assert not result.has_lexical
    assert not result.has_morphology
    assert not result.has_sandhi
    assert not result.has_samasa
    assert not result.has_semantic


def test_fully_resolved_is_false_initially():
    result = make_result()

    assert not result.fully_resolved


def test_diagnostic_properties():
    diagnostic = make_diagnostic()

    result = make_result(
        diagnostics=(diagnostic,),
    )

    assert result.has_diagnostics
    assert result.diagnostic_count == 1
    assert result.diagnostics == (diagnostic,)


def test_with_lexical_returns_new_result():
    result = make_result()
    lexical = object()

    enriched = result.with_lexical(lexical)

    assert enriched is not result
    assert enriched.lexical is lexical
    assert result.lexical is None


def test_with_morphology_preserves_existing_lexical_result():
    lexical = object()
    morphology = object()

    result = make_result(
        lexical=lexical,
    )

    enriched = result.with_morphology(
        morphology,
    )

    assert enriched.lexical is lexical
    assert enriched.morphology is morphology
    assert enriched.sandhi is None
    assert enriched.samasa is None
    assert enriched.semantic is None


def test_with_sandhi_preserves_previous_results():
    lexical = object()
    morphology = object()
    sandhi = object()

    result = make_result(
        lexical=lexical,
        morphology=morphology,
    )

    enriched = result.with_sandhi(sandhi)

    assert enriched.lexical is lexical
    assert enriched.morphology is morphology
    assert enriched.sandhi is sandhi


def test_with_samasa_preserves_previous_results():
    lexical = object()
    morphology = object()
    sandhi = object()
    samasa = object()

    result = make_result(
        lexical=lexical,
        morphology=morphology,
        sandhi=sandhi,
    )

    enriched = result.with_samasa(samasa)

    assert enriched.lexical is lexical
    assert enriched.morphology is morphology
    assert enriched.sandhi is sandhi
    assert enriched.samasa is samasa


def test_with_semantic_preserves_previous_results():
    lexical = object()
    morphology = object()
    sandhi = object()
    samasa = object()
    semantic = object()

    result = make_result(
        lexical=lexical,
        morphology=morphology,
        sandhi=sandhi,
        samasa=samasa,
    )

    enriched = result.with_semantic(semantic)

    assert enriched.lexical is lexical
    assert enriched.morphology is morphology
    assert enriched.sandhi is sandhi
    assert enriched.samasa is samasa
    assert enriched.semantic is semantic


def test_fully_resolved_requires_all_five_stages():
    result = make_result(
        lexical=object(),
        morphology=object(),
        sandhi=object(),
        samasa=object(),
        semantic=object(),
    )

    assert result.fully_resolved


def test_enrichment_preserves_context():
    result = make_result()

    enriched = result.with_lexical(object())

    assert enriched.context is result.context


def test_enrichment_preserves_diagnostics():
    diagnostic = make_diagnostic()

    result = make_result(
        diagnostics=(diagnostic,),
    )

    enriched = result.with_lexical(object())

    assert enriched.diagnostics == (diagnostic,)


def test_enrichment_preserves_confidence():
    result = make_result(
        confidence=0.75,
    )

    enriched = result.with_lexical(object())

    assert enriched.confidence == 0.75


def test_enrichment_preserves_success_state():
    result = make_result(
        succeeded=False,
    )

    enriched = result.with_lexical(object())

    assert enriched.succeeded is False


def test_result_is_immutable():
    result = make_result()

    with pytest.raises(FrozenInstanceError):
        result.confidence = 1.0


def test_result_is_slot_based():
    result = make_result()

    assert not hasattr(result, "__dict__")


def test_result_is_immutable_and_displayable():
    result = make_result()

    assert result.is_immutable is True
    assert result.is_displayable is True


def test_string_representation():
    result = make_result()

    assert str(result) == "Resolution Result"

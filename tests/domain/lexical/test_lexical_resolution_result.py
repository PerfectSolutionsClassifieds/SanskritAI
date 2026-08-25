
from types import SimpleNamespace

from SanskritAI.domain.lexical.lookup_candidate import (
    LookupCandidate,
)
from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)
from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


def make_context():
    return ResolutionContext(
        identifier="test-001",
        subject="रामः",
        language="Sanskrit",
        script="Devanagari",
    )


def make_candidate(
    score=0.95,
    sense=True,
):
    entry = SimpleNamespace(
        entry_id="mw-001",
        headword="राम",
        lexeme=SimpleNamespace(
            lemma="राम",
        ),
    )

    candidate_sense = (
        SimpleNamespace(
            context="context",
            source=SimpleNamespace(
                identifier="MW",
            ),
            definition="Rama",
            gloss="Rama",
        )
        if sense
        else None
    )

    return LookupCandidate(
        entry=entry,
        sense=candidate_sense,
        score=score,
        matched_word_form="रामः",
        normalized_word_form="राम",
    )


def test_empty_result():
    result = LexicalResolutionResult(
        context=make_context(),
    )

    assert result.has_candidates is False
    assert result.candidate_count == 0
    assert result.preferred_candidate is None
    assert result.preferred_entry is None
    assert result.preferred_sense is None
    assert result.resolved is False
    assert result.unresolved is True
    assert result.is_unique is False
    assert result.is_ambiguous is False


def test_result_with_candidate():
    candidate = make_candidate()

    result = LexicalResolutionResult(
        context=make_context(),
        candidates=(candidate,),
        matched_word_form="रामः",
        normalized_word_form="राम",
        ambiguity_detected=False,
        confidence=0.95,
        succeeded=True,
    )

    assert result.has_candidates is True
    assert result.candidate_count == 1
    assert result.preferred_candidate is candidate
    assert result.preferred_entry is candidate.entry
    assert result.preferred_sense is candidate.sense


def test_result_exposes_lexical_information():
    result = LexicalResolutionResult(
        context=make_context(),
        candidates=(make_candidate(),),
        succeeded=True,
        confidence=0.95,
    )

    assert result.headword == "राम"
    assert result.lemma == "राम"
    assert result.definition == "Rama"
    assert result.glossary == "Rama"
    assert result.resolved is True
    assert result.is_unique is True
    assert result.is_confident is True


def test_result_detects_ambiguity():
    first = make_candidate(0.90)
    second = make_candidate(0.80)

    result = LexicalResolutionResult(
        context=make_context(),
        candidates=(first, second),
        ambiguity_detected=True,
        confidence=0.90,
        succeeded=True,
    )

    assert result.candidate_count == 2
    assert result.is_ambiguous is True
    assert result.is_unique is False


def test_low_confidence_is_not_confident():
    result = LexicalResolutionResult(
        context=make_context(),
        candidates=(make_candidate(0.70),),
        confidence=0.70,
        succeeded=True,
    )

    assert result.is_confident is False


def test_display_text_for_resolved_result():
    result = LexicalResolutionResult(
        context=make_context(),
        candidates=(make_candidate(),),
        confidence=0.95,
        succeeded=True,
    )

    assert result.display_text == "राम → Rama"
    assert str(result) == result.display_text


def test_display_text_for_unresolved_result():
    result = LexicalResolutionResult(
        context=make_context(),
        succeeded=False,
    )

    assert result.display_text == "No lexical resolution"
    assert result.display_description == "Lexical resolution failed."

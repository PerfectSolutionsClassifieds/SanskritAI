
from types import SimpleNamespace

import pytest

from SanskritAI.domain.lexical.lookup_candidate import (
    LookupCandidate,
)


def make_entry():
    return SimpleNamespace(
        entry_id="mw-001",
        headword="राम",
    )


def test_candidate_defaults():
    entry = make_entry()

    candidate = LookupCandidate(
        entry=entry,
    )

    assert candidate.entry is entry
    assert candidate.sense is None
    assert candidate.score == 1.0
    assert candidate.matched_word_form == ""
    assert candidate.normalized_word_form == ""


def test_candidate_properties():
    entry = make_entry()

    candidate = LookupCandidate(
        entry=entry,
        score=0.85,
        matched_word_form="रामः",
        normalized_word_form="राम",
    )

    assert candidate.identifier == "mw-001"
    assert candidate.headword == "राम"
    assert candidate.confidence == 0.85
    assert candidate.has_sense is False


def test_candidate_with_sense():
    entry = make_entry()
    sense = SimpleNamespace()

    candidate = LookupCandidate(
        entry=entry,
        sense=sense,
        score=0.95,
    )

    assert candidate.has_sense is True
    assert candidate.sense is sense


def test_candidate_is_immutable():
    candidate = LookupCandidate(
        entry=make_entry(),
    )

    with pytest.raises(AttributeError):
        candidate.score = 0.5


def test_candidate_string_representation():
    candidate = LookupCandidate(
        entry=make_entry(),
        score=0.875,
    )

    assert str(candidate) == "LookupCandidate(राम, score=0.875)"

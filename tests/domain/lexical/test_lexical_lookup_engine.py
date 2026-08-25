
from types import SimpleNamespace
from unittest.mock import Mock

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)
from SanskritAI.domain.lexical.lookup_ranking_policy import (
    LookupRankingPolicy,
)
from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


def make_context(subject="रामः"):
    return ResolutionContext(
        identifier="test-001",
        subject=subject,
        language="Sanskrit",
        script="Devanagari",
    )


def make_entry(
    entry_id,
    headword,
):
    return SimpleNamespace(
        entry_id=entry_id,
        headword=headword,
    )


class StudRankingPolicy(LookupRankingPolicy):

    def __init__(self):
        self.received = None

    def rank(self, candidates):
        self.received = tuple(candidates)

        return tuple(
            sorted(
                self.received,
                key=lambda candidate: -candidate.score,
            )
        )


def test_engine_accepts_repository():
    repository = Mock()

    engine = LexicalLookupEngine(
        repository=repository,
    )

    assert engine.repository is repository
    assert engine.ranking_policy is not None


def test_lookup_with_no_entries():
    repository = Mock()

    repository.find_entries_by_word_form.return_value = ()

    engine = LexicalLookupEngine(
        repository=repository,
    )

    result = engine.lookup(
        make_context("रामः"),
    )

    assert result.succeeded is False
    assert result.candidate_count == 0
    assert result.confidence == 0.0
    assert result.ambiguity_detected is False

    repository.find_entries_by_word_form.assert_called_once_with(
        "रामः",
    )


def test_lookup_constructs_candidates():
    repository = Mock()

    entry = make_entry(
        "mw-001",
        "राम",
    )

    repository.find_entries_by_word_form.return_value = (
        entry,
    )

    engine = LexicalLookupEngine(
        repository=repository,
    )

    result = engine.lookup(
        make_context("रामः"),
    )

    assert result.succeeded is True
    assert result.candidate_count == 1
    assert result.matched_word_form == "रामः"
    assert result.normalized_word_form == "रामः"

    candidate = result.preferred_candidate

    assert candidate.entry is entry
    assert candidate.matched_word_form == "रामः"


def test_lookup_detects_ambiguity():
    repository = Mock()

    first = make_entry(
        "mw-001",
        "राम",
    )

    second = make_entry(
        "mw-002",
        "राम",
    )

    repository.find_entries_by_word_form.return_value = (
        first,
        second,
    )

    engine = LexicalLookupEngine(
        repository=repository,
    )

    result = engine.lookup(
        make_context("राम"),
    )

    assert result.succeeded is True
    assert result.candidate_count == 2
    assert result.ambiguity_detected is True


def test_custom_ranking_policy_is_used():
    repository = Mock()

    repository.find_entries_by_word_form.return_value = (
        make_entry("1", "राम"),
        make_entry("2", "हरि"),
    )

    policy = StudRankingPolicy()

    engine = LexicalLookupEngine(
        repository=repository,
        ranking_policy=policy,
    )

    result = engine.lookup(
        make_context("राम"),
    )

    assert policy.received is not None
    assert len(policy.received) == 2
    assert result.succeeded is True

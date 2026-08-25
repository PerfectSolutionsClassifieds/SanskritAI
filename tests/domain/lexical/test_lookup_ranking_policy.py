
from types import SimpleNamespace

import pytest

from SanskritAI.domain.lexical.lookup_candidate import (
    LookupCandidate,
)
from SanskritAI.domain.lexical.lookup_ranking_policy import (
    DefaultLookupRankingPolicy,
    LookupRankingPolicy,
)


def candidate(
    headword,
    score,
    identifier,
):
    entry = SimpleNamespace(
        entry_id=identifier,
        headword=headword,
    )

    return LookupCandidate(
        entry=entry,
        score=score,
    )


def test_default_policy_is_lookup_ranking_policy():
    policy = DefaultLookupRankingPolicy()

    assert isinstance(
        policy,
        LookupRankingPolicy,
    )


def test_higher_score_is_ranked_first():
    policy = DefaultLookupRankingPolicy()

    low = candidate("राम", 0.50, "1")
    high = candidate("हरि", 0.90, "2")

    ranked = policy.rank(
        [low, high],
    )

    assert ranked == (
        high,
        low,
    )


# def test_equal_scores_use_alphabetical_headword():
#     policy = DefaultLookupRankingPolicy()

#     first = candidate("हरि", 0.80, "1")
#     second = candidate("राम", 0.80, "2")

#     ranked = policy.rank(
#         [first, second],
#     )

#     assert ranked == (
#         first,
#         second,
#     )

def test_equal_scores_use_alphabetical_headword():
    policy = DefaultLookupRankingPolicy()

    first = candidate("हरि", 0.80, "1")
    second = candidate("राम", 0.80, "2")

    ranked = policy.rank(
        [first, second],
    )

    assert ranked == (
        second,
        first,
    )

def test_empty_candidates_return_empty_tuple():
    policy = DefaultLookupRankingPolicy()

    assert policy.rank([]) == ()


def test_generator_input_is_supported():
    policy = DefaultLookupRankingPolicy()

    candidates = [
        candidate("राम", 0.40, "1"),
        candidate("हरि", 0.90, "2"),
    ]

    ranked = policy.rank(
        candidate for candidate in candidates
    )

    assert ranked[0].headword == "हरि"

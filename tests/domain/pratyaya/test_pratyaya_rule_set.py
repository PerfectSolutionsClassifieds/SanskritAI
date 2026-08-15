
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_rule import PratyayaRule
from SanskritAI.domain.pratyaya.pratyaya_rule_set import PratyayaRuleSet


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------

@dataclass
class FakeContext:
    value: str = "context"


class FakePratyayaRule(PratyayaRule):
    """
    Minimal concrete rule used to test PratyayaRuleSet orchestration.

    The rule deliberately returns arbitrary candidate values so that the
    rule-set contract can be tested independently of individual Pratyaya
    rules.
    """

    def __init__(
        self,
        identifier: str,
        candidates: tuple[Any, ...] = (),
        applies: bool = True,
    ) -> None:
        self._identifier = identifier
        self._candidates = candidates
        self._applies = applies

    @property
    def identifier(self) -> str:
        return self._identifier

    def applies_to(self, context: PratyayaContext) -> bool:
        return self._applies

    def apply(self, context: PratyayaContext) -> tuple[Any, ...]:
        return self._candidates


def make_context() -> PratyayaContext:
    return PratyayaContext(
        identifier="pratyaya-test-1",
        subject="क्त",
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_empty_rule_set_is_empty():
    rule_set = PratyayaRuleSet()

    assert rule_set.is_empty
    assert rule_set.count == 0
    assert len(rule_set) == 0
    assert tuple(rule_set) == ()


def test_rule_set_stores_rules():
    rule = FakePratyayaRule(identifier="rule-1")

    rule_set = PratyayaRuleSet(
        rules=(rule,),
    )

    assert rule_set.count == 1
    assert len(rule_set) == 1
    assert rule_set[0] is rule


def test_iteration_preserves_rule_order():
    first = FakePratyayaRule(identifier="first")
    second = FakePratyayaRule(identifier="second")

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    assert tuple(rule_set) == (first, second)


def test_index_access_preserves_rule_order():
    first = FakePratyayaRule(identifier="first")
    second = FakePratyayaRule(identifier="second")

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    assert rule_set[0] is first
    assert rule_set[1] is second


# ---------------------------------------------------------------------------
# Immutability / add
# ---------------------------------------------------------------------------

def test_add_returns_new_rule_set():
    first = FakePratyayaRule(identifier="first")
    second = FakePratyayaRule(identifier="second")

    original = PratyayaRuleSet(
        rules=(first,),
    )

    updated = original.add(second)

    assert updated is not original
    assert original.rules == (first,)
    assert updated.rules == (first, second)


def test_add_preserves_existing_rule_order():
    first = FakePratyayaRule(identifier="first")
    second = FakePratyayaRule(identifier="second")
    third = FakePratyayaRule(identifier="third")

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    updated = rule_set.add(third)

    assert tuple(updated) == (first, second, third)


def test_rule_set_is_immutable():
    rule = FakePratyayaRule(identifier="rule-1")
    rule_set = PratyayaRuleSet(rules=(rule,))

    with pytest.raises(Exception):
        rule_set.rules = ()


# ---------------------------------------------------------------------------
# apply()
# ---------------------------------------------------------------------------

def test_apply_returns_empty_tuple_for_empty_rule_set():
    rule_set = PratyayaRuleSet()

    result = rule_set.apply(make_context())

    assert result == ()


def test_apply_invokes_matching_rules():
    first = FakePratyayaRule(
        identifier="first",
        candidates=("क्त",),
        applies=True,
    )
    second = FakePratyayaRule(
        identifier="second",
        candidates=("तव्य",),
        applies=True,
    )

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(make_context())

    assert result == ("क्त", "तव्य")


def test_apply_skips_non_matching_rules():
    matching = FakePratyayaRule(
        identifier="matching",
        candidates=("क्त",),
        applies=True,
    )
    non_matching = FakePratyayaRule(
        identifier="non-matching",
        candidates=("तव्य",),
        applies=False,
    )

    rule_set = PratyayaRuleSet(
        rules=(matching, non_matching),
    )

    result = rule_set.apply(make_context())

    assert result == ("क्त",)


def test_apply_preserves_candidate_insertion_order():
    first = FakePratyayaRule(
        identifier="first",
        candidates=("first", "second"),
    )
    second = FakePratyayaRule(
        identifier="second",
        candidates=("third", "fourth"),
    )

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(make_context())

    assert result == (
        "first",
        "second",
        "third",
        "fourth",
    )


def test_apply_deduplicates_hashable_candidates():
    first = FakePratyayaRule(
        identifier="first",
        candidates=("क्त", "तव्य"),
    )
    second = FakePratyayaRule(
        identifier="second",
        candidates=("क्त", "ल्युट्"),
    )

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(make_context())

    assert result == (
        "क्त",
        "तव्य",
        "ल्युट्",
    )


# ---------------------------------------------------------------------------
# Regression tests: unhashable candidates
# ---------------------------------------------------------------------------

def test_apply_supports_unhashable_candidates():
    """
    Regression test for the current production failure:

        tuple(dict.fromkeys(candidates))

    Dictionary candidates are unhashable and therefore must not cause
    PratyayaRuleSet.apply() to raise TypeError.
    """

    first_candidate = {
        "subject": "क्त",
        "surface": "भूत",
    }

    duplicate_candidate = {
        "subject": "क्त",
        "surface": "भूत",
    }

    second_candidate = {
        "subject": "तव्य",
        "surface": "भवितव्य",
    }

    first = FakePratyayaRule(
        identifier="first",
        candidates=(
            first_candidate,
            second_candidate,
        ),
    )

    second = FakePratyayaRule(
        identifier="second",
        candidates=(
            duplicate_candidate,
        ),
    )

    rule_set = PratyayaRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(make_context())

    assert result == (
        first_candidate,
        second_candidate,
    )


def test_apply_preserves_first_occurrence_of_unhashable_candidates():
    first_candidate = {
        "subject": "क्त",
        "surface": "भूत",
        "source": "first",
    }

    duplicate_candidate = {
        "subject": "क्त",
        "surface": "भूत",
        "source": "first",
    }

    rule_set = PratyayaRuleSet(
        rules=(
            FakePratyayaRule(
                identifier="first",
                candidates=(first_candidate,),
            ),
            FakePratyayaRule(
                identifier="second",
                candidates=(duplicate_candidate,),
            ),
        ),
    )

    result = rule_set.apply(make_context())

    assert result == (
        first_candidate,
    )


def test_apply_does_not_duplicate_identical_dictionary_candidates():
    candidate = {
        "subject": "क्त",
        "surface": "भूत",
        "confidence": 1.0,
    }

    rule_set = PratyayaRuleSet(
        rules=(
            FakePratyayaRule(
                identifier="rule-1",
                candidates=(candidate,),
            ),
            FakePratyayaRule(
                identifier="rule-2",
                candidates=(candidate,),
            ),
            FakePratyayaRule(
                identifier="rule-3",
                candidates=(candidate,),
            ),
        ),
    )

    result = rule_set.apply(make_context())

    assert result == (
        candidate,
    )


def test_apply_returns_tuple():
    rule = FakePratyayaRule(
        identifier="rule-1",
        candidates=(
            {"subject": "क्त"},
        ),
    )

    rule_set = PratyayaRuleSet(
        rules=(rule,),
    )

    result = rule_set.apply(make_context())

    assert isinstance(result, tuple)


def test_apply_does_not_retain_previous_results():
    first_candidate = {
        "subject": "क्त",
        "surface": "भूत",
    }

    second_candidate = {
        "subject": "तव्य",
        "surface": "भवितव्य",
    }

    rule_set = PratyayaRuleSet(
        rules=(
            FakePratyayaRule(
                identifier="rule-1",
                candidates=(first_candidate,),
            ),
        ),
    )

    first_result = rule_set.apply(make_context())

    assert first_result == (first_candidate,)

    # A new rule set represents a new evaluation independently.
    updated = PratyayaRuleSet(
        rules=(
            FakePratyayaRule(
                identifier="rule-2",
                candidates=(second_candidate,),
            ),
        ),
    )

    second_result = updated.apply(make_context())

    assert second_result == (second_candidate,)

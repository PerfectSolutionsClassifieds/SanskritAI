
from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.domain.derivation.derivation_rule import DerivationRule
from SanskritAI.domain.derivation.derivation_rule_set import DerivationRuleSet


@dataclass(frozen=True)
class FakeContext:
    value: str = "context"


class FakeRule(DerivationRule):
    """
    Minimal test rule used to verify DerivationRuleSet behavior
    independently of the concrete Sanskrit derivation rules.
    """

    def __init__(
        self,
        *,
        identifier: str,
        applies: bool = True,
        candidates: tuple[object, ...] = (),
    ) -> None:
        self._identifier = identifier
        self._applies = applies
        self._candidates = candidates
        self.apply_calls = 0
        self.applies_to_calls = 0

    @property
    def identifier(self) -> str:
        return self._identifier

    def applies_to(self, context) -> bool:
        self.applies_to_calls += 1
        return self._applies

    def apply(self, context) -> tuple[object, ...]:
        self.apply_calls += 1
        return self._candidates


def test_empty_rule_set_has_no_rules():
    rule_set = DerivationRuleSet()

    assert rule_set.rules == ()


def test_rule_set_accepts_rules():
    rule = FakeRule(identifier="rule-1")

    rule_set = DerivationRuleSet(
        rules=(rule,),
    )

    assert rule_set.rules == (rule,)


def test_apply_returns_no_candidates_for_empty_rule_set():
    rule_set = DerivationRuleSet()

    result = rule_set.apply(FakeContext())

    assert result == ()


def test_apply_checks_every_rule():
    first = FakeRule(
        identifier="rule-1",
        applies=True,
        candidates=("first",),
    )
    second = FakeRule(
        identifier="rule-2",
        applies=False,
        candidates=("second",),
    )
    third = FakeRule(
        identifier="rule-3",
        applies=True,
        candidates=("third",),
    )

    rule_set = DerivationRuleSet(
        rules=(first, second, third),
    )

    rule_set.apply(FakeContext())

    assert first.applies_to_calls == 1
    assert second.applies_to_calls == 1
    assert third.applies_to_calls == 1


def test_apply_only_applies_matching_rules():
    matching = FakeRule(
        identifier="matching",
        applies=True,
        candidates=("candidate",),
    )
    non_matching = FakeRule(
        identifier="non-matching",
        applies=False,
        candidates=("should-not-appear",),
    )

    rule_set = DerivationRuleSet(
        rules=(matching, non_matching),
    )

    result = rule_set.apply(FakeContext())

    assert result == ("candidate",)
    assert matching.apply_calls == 1
    assert non_matching.apply_calls == 0


def test_apply_preserves_rule_order():
    first = FakeRule(
        identifier="first",
        candidates=("first",),
    )
    second = FakeRule(
        identifier="second",
        candidates=("second",),
    )
    third = FakeRule(
        identifier="third",
        candidates=("third",),
    )

    rule_set = DerivationRuleSet(
        rules=(first, second, third),
    )

    result = rule_set.apply(FakeContext())

    assert result == (
        "first",
        "second",
        "third",
    )


def test_apply_preserves_candidate_order_within_rules():
    rule = FakeRule(
        identifier="rule-1",
        candidates=(
            "candidate-1",
            "candidate-2",
            "candidate-3",
        ),
    )

    rule_set = DerivationRuleSet(
        rules=(rule,),
    )

    result = rule_set.apply(FakeContext())

    assert result == (
        "candidate-1",
        "candidate-2",
        "candidate-3",
    )


def test_apply_removes_duplicate_hashable_candidates():
    first = FakeRule(
        identifier="first",
        candidates=(
            "shared",
            "first-only",
        ),
    )
    second = FakeRule(
        identifier="second",
        candidates=(
            "shared",
            "second-only",
        ),
    )

    rule_set = DerivationRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(FakeContext())

    assert result == (
        "shared",
        "first-only",
        "second-only",
    )


def test_apply_supports_unhashable_candidates():
    """
    Regression test for the current production failure:

        tuple(dict.fromkeys(candidates))

    cannot process dictionary candidates because dictionaries
    are unhashable.

    Concrete derivation rules currently return dictionary-shaped
    candidates, so DerivationRuleSet must support them.
    """

    first_candidate = {
        "surface": "भूत",
        "rule": "kta",
    }
    duplicate_candidate = {
        "surface": "भूत",
        "rule": "kta",
    }
    second_candidate = {
        "surface": "भवित",
        "rule": "kta",
    }

    first = FakeRule(
        identifier="first",
        candidates=(
            first_candidate,
            second_candidate,
        ),
    )
    second = FakeRule(
        identifier="second",
        candidates=(
            duplicate_candidate,
        ),
    )

    rule_set = DerivationRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(FakeContext())

    assert result == (
        first_candidate,
        second_candidate,
    )


def test_apply_preserves_first_occurrence_of_unhashable_candidates():
    first_candidate = {
        "surface": "भूत",
        "source": "first",
    }
    duplicate_candidate = {
        "surface": "भूत",
        "source": "first",
    }

    rule_set = DerivationRuleSet(
        rules=(
            FakeRule(
                identifier="first",
                candidates=(first_candidate,),
            ),
            FakeRule(
                identifier="second",
                candidates=(duplicate_candidate,),
            ),
        ),
    )

    result = rule_set.apply(FakeContext())

    assert len(result) == 1
    assert result[0] == first_candidate


def test_apply_does_not_duplicate_identical_candidates_from_multiple_rules():
    candidate = {
        "surface": "भूत",
        "confidence": 1.0,
    }

    rule_set = DerivationRuleSet(
        rules=(
            FakeRule(
                identifier="rule-1",
                candidates=(candidate,),
            ),
            FakeRule(
                identifier="rule-2",
                candidates=(candidate,),
            ),
            FakeRule(
                identifier="rule-3",
                candidates=(candidate,),
            ),
        ),
    )

    result = rule_set.apply(FakeContext())

    assert result == (candidate,)


def test_apply_does_not_mutate_rule_set():
    first = FakeRule(
        identifier="first",
        candidates=("first",),
    )
    second = FakeRule(
        identifier="second",
        candidates=("second",),
    )

    rule_set = DerivationRuleSet(
        rules=(first, second),
    )

    original_rules = rule_set.rules

    rule_set.apply(FakeContext())

    assert rule_set.rules == original_rules


def test_apply_can_be_called_multiple_times():
    rule = FakeRule(
        identifier="rule-1",
        candidates=("candidate",),
    )

    rule_set = DerivationRuleSet(
        rules=(rule,),
    )

    first_result = rule_set.apply(FakeContext())
    second_result = rule_set.apply(FakeContext())

    assert first_result == ("candidate",)
    assert second_result == ("candidate",)
    assert rule.apply_calls == 2


def test_apply_does_not_retain_previous_candidates():
    first = FakeRule(
        identifier="first",
        candidates=("first",),
    )

    rule_set = DerivationRuleSet(
        rules=(first,),
    )

    first_result = rule_set.apply(FakeContext())

    first._candidates = ("second",)

    second_result = rule_set.apply(FakeContext())

    assert first_result == ("first",)
    assert second_result == ("second",)


def test_non_matching_rules_are_not_applied_even_when_other_rules_match():
    matching = FakeRule(
        identifier="matching",
        applies=True,
        candidates=("accepted",),
    )
    non_matching = FakeRule(
        identifier="non-matching",
        applies=False,
        candidates=("rejected",),
    )

    rule_set = DerivationRuleSet(
        rules=(matching, non_matching),
    )

    result = rule_set.apply(FakeContext())

    assert result == ("accepted",)
    assert matching.apply_calls == 1
    assert non_matching.apply_calls == 0

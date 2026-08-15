
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet


@dataclass
class FakeSamasaRule(SamasaRule):
    """
    Minimal concrete SamasaRule used to test SamasaRuleSet
    independently from the concrete Samasa heuristics.
    """

    identifier: str
    candidates: tuple[Any, ...] = ()
    applicable: bool = True

    @property
    def display_name(self) -> str:
        return self.identifier

    def applies_to(
        self,
        context: SamasaContext,
    ) -> bool:
        return self.applicable

    def apply(
        self,
        context: SamasaContext,
    ) -> tuple[Any, ...]:
        return self.candidates


def make_context() -> SamasaContext:
    return SamasaContext(
        identifier="samasa-test-1",
        subject="राज पुरुष",
    )


def test_empty_rule_set():
    rule_set = SamasaRuleSet()

    assert rule_set.rules == ()
    assert rule_set.count == 0
    assert len(rule_set) == 0
    assert rule_set.is_empty is True


def test_rule_set_preserves_rule_order():
    first = FakeSamasaRule(identifier="first")
    second = FakeSamasaRule(identifier="second")
    third = FakeSamasaRule(identifier="third")

    rule_set = SamasaRuleSet(
        rules=(first, second, third),
    )

    assert rule_set.rules == (first, second, third)
    assert tuple(rule_set) == (first, second, third)
    assert rule_set[0] is first
    assert rule_set[1] is second
    assert rule_set[2] is third


def test_add_returns_new_rule_set():
    original = SamasaRuleSet()
    rule = FakeSamasaRule(identifier="tatpurusha")

    result = original.add(rule)

    assert original.rules == ()
    assert original.count == 0
    assert result.rules == (rule,)
    assert result.count == 1


def test_add_does_not_mutate_original_rule_set():
    first = FakeSamasaRule(identifier="first")
    second = FakeSamasaRule(identifier="second")

    original = SamasaRuleSet(
        rules=(first,),
    )

    result = original.add(second)

    assert original.rules == (first,)
    assert result.rules == (first, second)


def test_apply_ignores_non_matching_rules():
    matching = FakeSamasaRule(
        identifier="matching",
        candidates=(
            {"type": "Tatpurusha"},
        ),
        applicable=True,
    )

    non_matching = FakeSamasaRule(
        identifier="non-matching",
        candidates=(
            {"type": "ShouldNotAppear"},
        ),
        applicable=False,
    )

    rule_set = SamasaRuleSet(
        rules=(matching, non_matching),
    )

    result = rule_set.apply(make_context())

    assert result == (
        {"type": "Tatpurusha"},
    )


def test_apply_supports_unhashable_candidates():
    """
    Regression test for the production failure caused by:

        tuple(dict.fromkeys(candidates))

    Samasa rules intentionally return dictionary-shaped candidates,
    which are unhashable.
    """

    first_candidate = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
    }

    duplicate_candidate = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
    }

    second_candidate = {
        "type": "Dvandva",
        "compound": "राम कृष्ण",
    }

    first = FakeSamasaRule(
        identifier="first",
        candidates=(
            first_candidate,
            second_candidate,
        ),
    )

    second = FakeSamasaRule(
        identifier="second",
        candidates=(
            duplicate_candidate,
        ),
    )

    rule_set = SamasaRuleSet(
        rules=(first, second),
    )

    result = rule_set.apply(make_context())

    assert result == (
        first_candidate,
        second_candidate,
    )


def test_apply_preserves_first_occurrence_of_unhashable_candidates():
    first_candidate = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
        "source": "first",
    }

    duplicate_candidate = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
        "source": "first",
    }

    rule_set = SamasaRuleSet(
        rules=(
            FakeSamasaRule(
                identifier="first",
                candidates=(first_candidate,),
            ),
            FakeSamasaRule(
                identifier="second",
                candidates=(duplicate_candidate,),
            ),
        ),
    )

    result = rule_set.apply(make_context())

    assert len(result) == 1
    assert result[0] == first_candidate
    assert result[0] is first_candidate


def test_apply_does_not_duplicate_identical_dictionary_candidates():
    candidate = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
        "confidence": 1.0,
    }

    rule_set = SamasaRuleSet(
        rules=(
            FakeSamasaRule(
                identifier="rule-1",
                candidates=(candidate,),
            ),
            FakeSamasaRule(
                identifier="rule-2",
                candidates=(candidate,),
            ),
            FakeSamasaRule(
                identifier="rule-3",
                candidates=(candidate,),
            ),
        ),
    )

    result = rule_set.apply(make_context())

    assert result == (candidate,)
    assert len(result) == 1


def test_apply_preserves_candidate_insertion_order():
    first = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
    }

    second = {
        "type": "Dvandva",
        "compound": "राम कृष्ण",
    }

    third = {
        "type": "Bahuvrihi",
        "compound": "पीत अम्बर",
    }

    rule_set = SamasaRuleSet(
        rules=(
            FakeSamasaRule(
                identifier="rule-1",
                candidates=(first, second),
            ),
            FakeSamasaRule(
                identifier="rule-2",
                candidates=(third,),
            ),
        ),
    )

    result = rule_set.apply(make_context())

    assert result == (
        first,
        second,
        third,
    )


def test_apply_returns_tuple():
    rule = FakeSamasaRule(
        identifier="rule-1",
        candidates=(
            {"type": "Tatpurusha"},
        ),
    )

    rule_set = SamasaRuleSet(
        rules=(rule,),
    )

    result = rule_set.apply(make_context())

    assert isinstance(result, tuple)


def test_apply_does_not_retain_previous_results():
    first_candidate = {
        "type": "Tatpurusha",
        "compound": "राज पुरुष",
    }

    second_candidate = {
        "type": "Dvandva",
        "compound": "राम कृष्ण",
    }

    rule = FakeSamasaRule(
        identifier="rule-1",
        candidates=(first_candidate,),
    )

    rule_set = SamasaRuleSet(
        rules=(rule,),
    )

    first_result = rule_set.apply(make_context())

    rule.candidates = (second_candidate,)

    second_result = rule_set.apply(make_context())

    assert first_result == (first_candidate,)
    assert second_result == (second_candidate,)


def test_display_name():
    rule_set = SamasaRuleSet()

    assert rule_set.display_name == "Samasa Rule Set"


def test_display_text():
    rule_set = SamasaRuleSet(
        rules=(
            FakeSamasaRule(identifier="first"),
            FakeSamasaRule(identifier="second"),
        ),
    )

    assert rule_set.display_text == "2 Samasa Rules"


def test_display_description():
    rule_set = SamasaRuleSet()

    assert (
        rule_set.display_description
        == "Immutable collection of Samasa rules."
    )


def test_str_uses_display_text():
    rule_set = SamasaRuleSet(
        rules=(
            FakeSamasaRule(identifier="first"),
        ),
    )

    assert str(rule_set) == "1 Samasa Rules"


from __future__ import annotations

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)
from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


class MatchingRule(SandhiRule):
    """Test rule that always applies."""

    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:
        return True

    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        return (
            "देवः अस्ति",
            "देवोऽस्ति",
        )


class NonMatchingRule(SandhiRule):
    """Test rule that never applies."""

    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:
        return False

    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        return (
            "SHOULD-NOT-APPEAR",
        )


class DuplicateOutputRule(SandhiRule):
    """Test rule producing duplicate candidates."""

    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:
        return True

    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        return (
            "देवोऽस्ति",
            "हरिरस्ति",
            "देवः अस्ति",
        )


def make_context() -> SandhiContext:
    return SandhiContext(
        identifier="context-1",
        subject="देवोऽस्ति",
    )


def test_default_rule_set_is_empty():
    rule_set = SandhiRuleSet()

    assert rule_set.rules == ()
    assert rule_set.is_empty is True
    assert rule_set.count == 0


def test_rule_set_is_immutable():
    rule_set = SandhiRuleSet()

    assert rule_set.is_immutable is True


def test_rule_set_is_slot_based():
    rule_set = SandhiRuleSet()

    assert not hasattr(
        rule_set,
        "__dict__",
    )


def test_rule_set_display_name():
    rule_set = SandhiRuleSet()

    assert (
        rule_set.display_name
        == "Sandhi Rule Set"
    )


def test_rule_set_display_text_for_empty_set():
    rule_set = SandhiRuleSet()

    assert (
        rule_set.display_text
        == "0 Sandhi Rules"
    )


def test_rule_set_display_description():
    rule_set = SandhiRuleSet()

    assert (
        rule_set.display_description
        == "Immutable collection of Sandhi rules."
    )


def test_rule_set_string_representation():
    rule_set = SandhiRuleSet()

    assert str(rule_set) == "0 Sandhi Rules"


def test_add_returns_new_rule_set():
    rule_set = SandhiRuleSet()
    rule = MatchingRule()

    updated = rule_set.add(rule)

    assert updated is not rule_set
    assert rule_set.is_empty is True
    assert updated.count == 1
    assert updated[0] is rule


def test_add_preserves_existing_rules():
    first = MatchingRule()
    second = NonMatchingRule()

    rule_set = SandhiRuleSet(
        rules=(first,),
    )

    updated = rule_set.add(second)

    assert updated.rules == (
        first,
        second,
    )


def test_add_does_not_mutate_original_rule_set():
    rule = MatchingRule()
    rule_set = SandhiRuleSet()

    updated = rule_set.add(rule)

    assert rule_set.count == 0
    assert updated.count == 1


def test_apply_uses_matching_rules_only():
    rule_set = SandhiRuleSet(
        rules=(
            MatchingRule(),
            NonMatchingRule(),
        ),
    )

    result = rule_set.apply(
        make_context(),
    )

    assert result == (
        "देवः अस्ति",
        "देवोऽस्ति",
    )


def test_apply_collects_outputs_from_all_matching_rules():
    rule_set = SandhiRuleSet(
        rules=(
            MatchingRule(),
            DuplicateOutputRule(),
        ),
    )

    result = rule_set.apply(
        make_context(),
    )

    assert result == (
        "देवः अस्ति",
        "देवोऽस्ति",
        "हरिरस्ति",
    )


def test_apply_removes_duplicates_preserving_order():
    rule_set = SandhiRuleSet(
        rules=(
            MatchingRule(),
            DuplicateOutputRule(),
        ),
    )

    result = rule_set.apply(
        make_context(),
    )

    assert result == (
        "देवः अस्ति",
        "देवोऽस्ति",
        "हरिरस्ति",
    )


def test_apply_empty_rule_set_returns_empty_tuple():
    rule_set = SandhiRuleSet()

    result = rule_set.apply(
        make_context(),
    )

    assert result == ()
    assert isinstance(result, tuple)


def test_len_returns_rule_count():
    rule_set = SandhiRuleSet(
        rules=(
            MatchingRule(),
            NonMatchingRule(),
        ),
    )

    assert len(rule_set) == 2


def test_iteration_returns_rules_in_order():
    first = MatchingRule()
    second = NonMatchingRule()

    rule_set = SandhiRuleSet(
        rules=(
            first,
            second,
        ),
    )

    assert tuple(rule_set) == (
        first,
        second,
    )


def test_indexing_returns_rule():
    first = MatchingRule()
    second = NonMatchingRule()

    rule_set = SandhiRuleSet(
        rules=(
            first,
            second,
        ),
    )

    assert rule_set[0] is first
    assert rule_set[1] is second


def test_display_text_reflects_rule_count():
    rule_set = SandhiRuleSet(
        rules=(
            MatchingRule(),
            NonMatchingRule(),
            DuplicateOutputRule(),
        ),
    )

    assert (
        rule_set.display_text
        == "3 Sandhi Rules"
    )


def test_rule_set_is_displayable():
    rule_set = SandhiRuleSet()

    assert rule_set.is_displayable is True


def test_to_display_string_returns_display_text():
    rule_set = SandhiRuleSet(
        rules=(
            MatchingRule(),
        ),
    )

    assert (
        rule_set.to_display_string()
        == rule_set.display_text
    )

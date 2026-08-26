
from __future__ import annotations

import pytest

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)


class ConcreteSandhiRule(SandhiRule):
    """
    Minimal concrete implementation used only to test
    the SandhiRule abstract contract.
    """

    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:
        return context.subject == "देवोऽस्ति"

    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        if self.applies_to(context):
            return ("देवः अस्ति",)

        return ()


def make_context(
    subject: str = "देवोऽस्ति",
) -> SandhiContext:
    return SandhiContext(
        identifier="context-1",
        subject=subject,
    )


def test_sandhi_rule_is_abstract():
    assert getattr(
        SandhiRule,
        "__abstractmethods__",
    ) == {
        "applies_to",
        "apply",
    }


def test_sandhi_rule_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        SandhiRule()


def test_concrete_rule_is_instance_of_sandhi_rule():
    rule = ConcreteSandhiRule()

    assert isinstance(
        rule,
        SandhiRule,
    )


def test_rule_display_name_defaults_to_class_name():
    rule = ConcreteSandhiRule()

    assert rule.display_name == "ConcreteSandhiRule"


def test_rule_display_text_delegates_to_display_name():
    rule = ConcreteSandhiRule()

    assert rule.display_text == rule.display_name


def test_rule_display_description_is_canonical():
    rule = ConcreteSandhiRule()

    assert (
        rule.display_description
        == "Abstract Sandhi rule."
    )


def test_rule_is_displayable():
    rule = ConcreteSandhiRule()

    assert rule.is_displayable is True


def test_rule_to_display_string_returns_display_text():
    rule = ConcreteSandhiRule()

    assert (
        rule.to_display_string()
        == rule.display_text
    )


def test_rule_applies_to_matching_context():
    rule = ConcreteSandhiRule()
    context = make_context()

    assert rule.applies_to(context) is True


def test_rule_does_not_apply_to_non_matching_context():
    rule = ConcreteSandhiRule()
    context = make_context("रामः गच्छति")

    assert rule.applies_to(context) is False


def test_rule_apply_returns_tuple_of_candidates():
    rule = ConcreteSandhiRule()
    context = make_context()

    result = rule.apply(context)

    assert result == ("देवः अस्ति",)
    assert isinstance(result, tuple)


def test_rule_apply_returns_empty_tuple_when_not_applicable():
    rule = ConcreteSandhiRule()
    context = make_context("रामः गच्छति")

    result = rule.apply(context)

    assert result == ()
    assert isinstance(result, tuple)


def test_rule_string_representation_uses_display_text():
    rule = ConcreteSandhiRule()

    assert str(rule) == rule.display_text


def test_rule_is_stateless():
    rule = ConcreteSandhiRule()
    context = make_context()

    first = rule.apply(context)
    second = rule.apply(context)

    assert first == second


def test_rule_preserves_context_contract():
    rule = ConcreteSandhiRule()
    context = make_context()

    assert isinstance(
        context,
        SandhiContext,
    )

    assert rule.applies_to(context) is True

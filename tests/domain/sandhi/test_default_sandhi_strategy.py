
from __future__ import annotations

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


def make_context():

    return SandhiContext(
        identifier="test-sandhi",
        subject="देव + इन्द्र",
        source="unit-test",
        language="sa",
        script="Devanagari",
        metadata={},
    )


def test_default_strategy_can_be_constructed():

    strategy = DefaultSandhiStrategy()

    assert strategy is not None


def test_default_strategy_uses_default_rule_set():

    strategy = DefaultSandhiStrategy()

    assert isinstance(
        strategy.rule_set,
        SandhiRuleSet,
    )


def test_default_strategy_accepts_explicit_rule_set():

    rule_set = SandhiRuleSet(
        rules=(),
    )

    strategy = DefaultSandhiStrategy(
        rule_set=rule_set,
    )

    assert strategy.rule_set is rule_set


def test_default_strategy_display_name():

    strategy = DefaultSandhiStrategy()

    assert strategy.display_name == (
        "Default Sandhi Strategy"
    )


def test_default_strategy_display_text():

    strategy = DefaultSandhiStrategy()

    assert strategy.display_text == (
        strategy.display_name
    )


def test_default_strategy_display_description():

    strategy = DefaultSandhiStrategy()

    assert strategy.display_description == (
        "Rule-based Sandhi strategy using the canonical "
        "Sandhi rule set."
    )


def test_default_strategy_resolve_returns_sandhi_result():

    strategy = DefaultSandhiStrategy()

    result = strategy.resolve(
        make_context(),
    )

    assert isinstance(
        result,
        SandhiResult,
    )


def test_default_strategy_result_preserves_context():

    context = make_context()

    strategy = DefaultSandhiStrategy()

    result = strategy.resolve(
        context,
    )

    assert result.context is context


def test_default_strategy_result_preserves_identifier():

    context = make_context()

    strategy = DefaultSandhiStrategy()

    result = strategy.resolve(
        context,
    )

    assert result.identifier == context.identifier


def test_default_strategy_empty_rule_set_produces_failure():

    strategy = DefaultSandhiStrategy(
        rule_set=SandhiRuleSet(
            rules=(),
        ),
    )

    context = make_context()

    result = strategy.resolve(
        context,
    )

    assert result.succeeded is False
    assert result.confidence == 0.0
    assert result.value == tuple()


def test_default_strategy_empty_rule_set_produces_diagnostic():

    strategy = DefaultSandhiStrategy(
        rule_set=SandhiRuleSet(
            rules=(),
        ),
    )

    result = strategy.resolve(
        make_context(),
    )

    assert result.has_diagnostics
    assert result.diagnostic_count == 1

    diagnostic = result.first_diagnostic

    assert diagnostic is not None
    assert diagnostic.code == (
        "SANDHI_NO_CANDIDATES"
    )
    assert diagnostic.severity == "WARNING"
    assert diagnostic.rule == (
        strategy.display_name
    )


def test_default_strategy_empty_rule_set_is_unresolved():

    strategy = DefaultSandhiStrategy(
        rule_set=SandhiRuleSet(
            rules=(),
        ),
    )

    result = strategy.resolve(
        make_context(),
    )

    assert result.resolved is False
    assert result.unresolved is True


def test_default_strategy_uses_one_confidence_for_single_candidate():

    strategy = DefaultSandhiStrategy()

    result = strategy.resolve(
        make_context(),
    )

    if result.succeeded and result.candidate_count == 1:
        assert result.confidence == 1.0


def test_default_strategy_multiple_candidates_use_lower_confidence():

    strategy = DefaultSandhiStrategy()

    result = strategy.resolve(
        make_context(),
    )

    if result.succeeded and result.candidate_count > 1:
        assert result.confidence == 0.75


def test_default_strategy_success_has_no_diagnostics():

    strategy = DefaultSandhiStrategy()

    result = strategy.resolve(
        make_context(),
    )

    if result.succeeded:
        assert result.diagnostics == tuple()

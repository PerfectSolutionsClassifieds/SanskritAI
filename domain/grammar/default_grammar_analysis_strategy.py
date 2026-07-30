from __future__ import annotations

"""
SanskritAI
==========

Default Grammar Analysis Strategy

Canonical grammar analysis strategy built on top of a
GrammarRuleSet.

This implementation delegates analysis to the reusable
canonical rule bundle and returns a GrammarAnalysisResult.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.grammar.default_grammar_rule_set import (
    default_grammar_rule_set,
)
from SanskritAI.domain.grammar.grammar_analysis_result import (
    GrammarAnalysisResult,
)
from SanskritAI.domain.grammar.grammar_analysis_strategy import (
    GrammarAnalysisStrategy,
)
from SanskritAI.domain.grammar.grammar_rule_set import GrammarRuleSet


class DefaultGrammarAnalysisStrategy(
    GrammarAnalysisStrategy,
):
    """
    Default rule-based grammar analysis strategy.
    """

    def __init__(
        self,
        rule_set: GrammarRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_grammar_rule_set()
        )

    @property
    def rule_set(self) -> GrammarRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Grammar Analysis Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Rule-based grammar analysis strategy using the "
            "canonical grammar rule set."
        )

    def analyze(
        self,
        subject: Any,
    ) -> GrammarAnalysisResult:
        """
        Analyzes the supplied subject using the configured rule set.
        """
        outputs = self.rule_set.apply(subject)

        confidence = (
            1.0
            if len(outputs) == 1
            else 0.75
            if len(outputs) > 1
            else 0.0
        )

        return GrammarAnalysisResult(
            subject=subject,
            outputs=outputs,
            analyzer=self.display_name,
            confidence=confidence,
            notes=(
                "Grammar analysis produced by the canonical "
                "rule bundle."
            ),
        )

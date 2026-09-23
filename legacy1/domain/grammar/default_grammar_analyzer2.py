from __future__ import annotations

"""
SanskritAI
==========

Default Grammar Analyzer

Canonical grammar analyzer built on top of a GrammarRuleSet.

This implementation mirrors the Morphology Kernel pattern:
a thin analyzer delegates to a reusable rule set.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.grammar.default_grammar_rule_set import (
    default_grammar_rule_set,
)
from SanskritAI.domain.grammar.grammar_analysis_result import (
    GrammarAnalysisResult,
)
from SanskritAI.domain.grammar.grammar_analyzer import GrammarAnalyzer
from SanskritAI.domain.grammar.grammar_rule_set import GrammarRuleSet


@dataclass(frozen=True, slots=True)
class DefaultGrammarAnalyzer(
    GrammarAnalyzer,
):
    """
    Default rule-based grammar analyzer.
    """

    rule_set: GrammarRuleSet = field(
        default_factory=default_grammar_rule_set,
    )

    @property
    def display_name(self) -> str:
        return "Default Grammar Analyzer"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Rule-based grammar analyzer using a GrammarRuleSet."

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
                "rule set."
            ),
        )

from __future__ import annotations

"""
SanskritAI
==========

Default Grammar Analyzer

Canonical grammar analyzer façade.

This implementation keeps the analyzer thin and delegates all
analysis work to the configured GrammarAnalysisStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.grammar.default_grammar_analysis_strategy import (
    DefaultGrammarAnalysisStrategy,
)
from SanskritAI.domain.grammar.grammar_analyzer import GrammarAnalyzer
from SanskritAI.domain.grammar.grammar_analysis_strategy import (
    GrammarAnalysisStrategy,
)


class DefaultGrammarAnalyzer(
    GrammarAnalyzer,
):
    """
    Default grammar analyzer façade.
    """

    def __init__(
        self,
        strategy: GrammarAnalysisStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultGrammarAnalysisStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Grammar Analyzer"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin grammar analyzer façade over the canonical "
            "grammar analysis strategy."
        )

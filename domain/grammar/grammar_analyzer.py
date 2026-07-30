from __future__ import annotations

"""
SanskritAI
==========

Grammar Analyzer

Defines the abstract grammar analyzer façade.

A GrammarAnalyzer delegates actual analysis work to a
GrammarAnalysisStrategy, keeping the analyzer thin and
consistent with the strategy/facade pattern used elsewhere in
SanskritAI.

Version
-------
v1.0.0
"""

from abc import ABC
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.grammar.grammar_analysis_result import (
    GrammarAnalysisResult,
)
from SanskritAI.domain.grammar.grammar_analysis_strategy import (
    GrammarAnalysisStrategy,
)


class GrammarAnalyzer(
    ABC,
    Displayable,
):
    """
    Abstract grammar analyzer façade.
    """

    def __init__(
        self,
        strategy: GrammarAnalysisStrategy,
    ) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> GrammarAnalysisStrategy:
        return self._strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract grammar analyzer."

    def analyze(
        self,
        subject: Any,
    ) -> GrammarAnalysisResult:
        """
        Analyzes the supplied subject by delegating to the
        configured strategy.
        """
        return self.strategy.analyze(subject)

    def __str__(self) -> str:
        return self.display_text

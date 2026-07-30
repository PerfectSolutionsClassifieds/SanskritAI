from __future__ import annotations

"""
SanskritAI
==========

Grammar Analyzer

Defines the abstract grammar analyzer.

A GrammarAnalyzer evaluates a subject using a GrammarRuleSet
and produces a GrammarAnalysisResult.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.grammar.grammar_analysis_result import (
    GrammarAnalysisResult,
)


class GrammarAnalyzer(
    ABC,
    Displayable,
):
    """
    Abstract grammar analyzer.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract grammar analyzer."

    @abstractmethod
    def analyze(
        self,
        subject: Any,
    ) -> GrammarAnalysisResult:
        """
        Analyzes the supplied subject and returns a grammar result.
        """
        raise NotImplementedError

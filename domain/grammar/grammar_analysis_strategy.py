from __future__ import annotations

"""
SanskritAI
==========

Grammar Analysis Strategy

Defines the abstract strategy responsible for analyzing a
grammar subject.

A GrammarAnalysisStrategy specializes the grammar analysis
workflow by producing a GrammarAnalysisResult from a subject.

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


class GrammarAnalysisStrategy(
    ABC,
    Displayable,
):
    """
    Abstract grammar analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract grammar analysis strategy."

    @abstractmethod
    def analyze(
        self,
        subject: Any,
    ) -> GrammarAnalysisResult:
        """
        Analyzes the supplied subject.
        """
        raise NotImplementedError

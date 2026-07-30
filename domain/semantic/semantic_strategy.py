from __future__ import annotations

"""
SanskritAI
==========

Semantic Strategy

Defines the abstract strategy for semantic analysis.

A SemanticStrategy encapsulates the algorithm responsible for
interpreting meaning and returning a SemanticResult.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_result import SemanticResult


class SemanticStrategy(
    ABC,
    Displayable,
):
    """
    Abstract semantic analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract semantic analysis strategy."

    @abstractmethod
    def analyze(self, context: SemanticContext) -> SemanticResult:
        """
        Analyzes the supplied semantic context.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

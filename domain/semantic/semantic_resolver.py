from __future__ import annotations

"""
SanskritAI
==========

Semantic Resolver

Defines the façade for semantic resolution.

SemanticResolver delegates all meaning-analysis work to a
configured SemanticStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_result import SemanticResult
from SanskritAI.domain.semantic.semantic_strategy import SemanticStrategy


class SemanticResolver(
    Displayable,
):
    """
    Canonical façade for semantic resolution.
    """

    def __init__(self, strategy: SemanticStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates semantic analysis to a strategy."

    @property
    def strategy(self) -> SemanticStrategy:
        return self._strategy

    def analyze(self, context: SemanticContext) -> SemanticResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

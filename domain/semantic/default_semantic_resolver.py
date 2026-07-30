from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Resolver

Canonical semantic resolver façade.

Version
-------
v1.0.0
"""

from SanskritAI.domain.semantic.default_semantic_strategy import (
    DefaultSemanticStrategy,
)
from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_resolver import SemanticResolver
from SanskritAI.domain.semantic.semantic_result import SemanticResult
from SanskritAI.domain.semantic.semantic_strategy import SemanticStrategy


class DefaultSemanticResolver(
    SemanticResolver,
):
    """
    Default Semantic resolver façade.
    """

    def __init__(
        self,
        strategy: SemanticStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultSemanticStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Semantic Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin Semantic resolver façade over the canonical "
            "Semantic strategy."
        )

    def analyze(self, context: SemanticContext) -> SemanticResult:
        return self.strategy.analyze(context)

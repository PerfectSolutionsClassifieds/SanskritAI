from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Resolver

Canonical derivation resolver façade.

This implementation keeps the resolver thin and delegates all
derivation work to the configured DerivationStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.derivation.default_derivation_strategy import (
    DefaultDerivationStrategy,
)
from SanskritAI.domain.derivation.derivation_context import DerivationContext
from SanskritAI.domain.derivation.derivation_resolver import DerivationResolver
from SanskritAI.domain.derivation.derivation_result import DerivationResult
from SanskritAI.domain.derivation.derivation_strategy import DerivationStrategy


class DefaultDerivationResolver(
    DerivationResolver,
):
    """
    Default derivation resolver façade.
    """

    def __init__(
        self,
        strategy: DerivationStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultDerivationStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Derivation Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin derivation resolver façade over the canonical "
            "derivation strategy."
        )

    def analyze(
        self,
        context: DerivationContext,
    ) -> DerivationResult:
        """
        Analyzes the supplied derivation context.
        """
        return self.strategy.analyze(context)

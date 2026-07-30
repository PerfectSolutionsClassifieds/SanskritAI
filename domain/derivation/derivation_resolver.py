from __future__ import annotations

"""
SanskritAI
==========

Derivation Resolver

Defines the façade for morphological derivation.

DerivationResolver delegates all derivational work to a
configured DerivationStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.derivation.derivation_context import DerivationContext
from SanskritAI.domain.derivation.derivation_result import DerivationResult
from SanskritAI.domain.derivation.derivation_strategy import DerivationStrategy


class DerivationResolver(
    Displayable,
):
    """
    Canonical façade for derivation resolution.
    """

    def __init__(
        self,
        strategy: DerivationStrategy,
    ) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates derivation analysis to a strategy."

    @property
    def strategy(self) -> DerivationStrategy:
        return self._strategy

    def analyze(
        self,
        context: DerivationContext,
    ) -> DerivationResult:
        """
        Analyzes the supplied derivation context.
        """
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

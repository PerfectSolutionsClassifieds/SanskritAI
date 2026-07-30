from __future__ import annotations

"""
SanskritAI
==========

Vakya Resolver

Defines the façade for sentence-level analysis.

This resolver now defaults to the canonical Vakya strategy so
both the strategy path and the analyzer path share the same
rule bundle.

Version
-------
v1.1.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.vakya.default_vakya_strategy import (
    DefaultVakyaStrategy,
)
from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_result import VakyaResult
from SanskritAI.domain.vakya.vakya_strategy import VakyaStrategy


class VakyaResolver(
    Displayable,
):
    """
    Canonical façade for Vakya resolution.
    """

    def __init__(
        self,
        strategy: VakyaStrategy | None = None,
    ) -> None:
        self._strategy = (
            strategy
            if strategy is not None
            else DefaultVakyaStrategy()
        )

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates Vakya analysis to a strategy."

    @property
    def strategy(self) -> VakyaStrategy:
        return self._strategy

    def analyze(self, context: VakyaContext) -> VakyaResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

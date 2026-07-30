from __future__ import annotations

"""
SanskritAI
==========

Default Vakya Resolver

Canonical sentence-analysis resolver façade.

This is a tiny wrapper over DefaultVakyaStrategy so the Vakya
Kernel follows the same pattern used in Dhatu, Pratyaya,
Samasa, and Derivation.

Version
-------
v1.0.0
"""

from SanskritAI.domain.vakya.default_vakya_strategy import (
    DefaultVakyaStrategy,
)
from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_resolver import VakyaResolver
from SanskritAI.domain.vakya.vakya_result import VakyaResult
from SanskritAI.domain.vakya.vakya_strategy import VakyaStrategy


class DefaultVakyaResolver(
    VakyaResolver,
):
    """
    Default Vakya resolver façade.
    """

    def __init__(
        self,
        strategy: VakyaStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultVakyaStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Vakya Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin Vakya resolver façade over the canonical "
            "Vakya strategy."
        )

    def analyze(
        self,
        context: VakyaContext,
    ) -> VakyaResult:
        """
        Analyzes the supplied Vakya context.
        """
        return self.strategy.analyze(context)

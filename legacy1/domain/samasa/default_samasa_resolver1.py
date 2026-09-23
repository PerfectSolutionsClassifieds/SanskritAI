from __future__ import annotations

"""
SanskritAI
==========

Default Samasa Resolver

Canonical Samasa resolver façade.

This implementation keeps the resolver thin and delegates all
Samasa work to the configured SamasaStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.samasa.default_samasa_strategy import (
    DefaultSamasaStrategy,
)
from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_resolver import SamasaResolver
from SanskritAI.domain.samasa.samasa_result import SamasaResult
from SanskritAI.domain.samasa.samasa_strategy import SamasaStrategy


class DefaultSamasaResolver(
    SamasaResolver,
):
    """
    Default Samasa resolver façade.
    """

    def __init__(
        self,
        strategy: SamasaStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultSamasaStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Samasa Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin Samasa resolver façade over the canonical "
            "Samasa strategy."
        )

    def analyze(
        self,
        context: SamasaContext,
    ) -> SamasaResult:
        """
        Analyzes the supplied Samasa context.
        """
        return self.strategy.analyze(context)

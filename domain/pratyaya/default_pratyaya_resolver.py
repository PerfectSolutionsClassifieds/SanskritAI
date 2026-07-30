from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Resolver

Canonical Pratyaya resolver façade.

This implementation keeps the resolver thin and delegates all
Pratyaya work to the configured PratyayaStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.pratyaya.default_pratyaya_strategy import (
    DefaultPratyayaStrategy,
)
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_resolver import PratyayaResolver
from SanskritAI.domain.pratyaya.pratyaya_result import PratyayaResult
from SanskritAI.domain.pratyaya.pratyaya_strategy import PratyayaStrategy


class DefaultPratyayaResolver(
    PratyayaResolver,
):
    """
    Default Pratyaya resolver façade.
    """

    def __init__(
        self,
        strategy: PratyayaStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultPratyayaStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Pratyaya Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin Pratyaya resolver façade over the canonical "
            "Pratyaya strategy."
        )

    def analyze(
        self,
        context: PratyayaContext,
    ) -> PratyayaResult:
        """
        Analyzes the supplied Pratyaya context.
        """
        return self.strategy.analyze(context)

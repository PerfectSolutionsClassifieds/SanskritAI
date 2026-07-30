from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Resolver

Canonical Dhatu resolver façade.

This implementation keeps the resolver thin and delegates all
Dhatu work to the configured DhatuStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.dhatu.default_dhatu_strategy import (
    DefaultDhatuStrategy,
)
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_resolver import DhatuResolver
from SanskritAI.domain.dhatu.dhatu_result import DhatuResult
from SanskritAI.domain.dhatu.dhatu_strategy import DhatuStrategy


class DefaultDhatuResolver(
    DhatuResolver,
):
    """
    Default Dhatu resolver façade.
    """

    def __init__(
        self,
        strategy: DhatuStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultDhatuStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Dhatu Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin Dhatu resolver façade over the canonical "
            "Dhatu strategy."
        )

    def analyze(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Analyzes the supplied Dhatu context.
        """
        return self.strategy.analyze(context)

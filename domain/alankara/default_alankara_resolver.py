from __future__ import annotations

"""
SanskritAI
==========

Default Alankara Resolver

Canonical Alankara resolver façade.

Version
-------
v1.0.0
"""

from SanskritAI.domain.alankara.alankara_context import AlankaraContext
from SanskritAI.domain.alankara.alankara_resolver import AlankaraResolver
from SanskritAI.domain.alankara.alankara_result import AlankaraResult
from SanskritAI.domain.alankara.alankara_strategy import AlankaraStrategy
from SanskritAI.domain.alankara.default_alankara_strategy import (
    DefaultAlankaraStrategy,
)


class DefaultAlankaraResolver(
    AlankaraResolver,
):
    """
    Default Alankara resolver façade.
    """

    def __init__(
        self,
        strategy: AlankaraStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultAlankaraStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Alankara Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Thin Alankara resolver façade over the canonical strategy."

    def analyze(self, context: AlankaraContext) -> AlankaraResult:
        return self.strategy.analyze(context)

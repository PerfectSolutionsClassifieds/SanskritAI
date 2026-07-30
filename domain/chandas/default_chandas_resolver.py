from __future__ import annotations

"""
SanskritAI
==========

Default Chandas Resolver

Canonical Chandas resolver façade.

Version
-------
v1.0.0
"""

from SanskritAI.domain.chandas.chandas_context import ChandasContext
from SanskritAI.domain.chandas.chandas_resolver import ChandasResolver
from SanskritAI.domain.chandas.chandas_result import ChandasResult
from SanskritAI.domain.chandas.chandas_strategy import ChandasStrategy
from SanskritAI.domain.chandas.default_chandas_strategy import (
    DefaultChandasStrategy,
)


class DefaultChandasResolver(
    ChandasResolver,
):
    """
    Default Chandas resolver façade.
    """

    def __init__(
        self,
        strategy: ChandasStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultChandasStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Chandas Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Thin Chandas resolver façade over the canonical strategy."

    def analyze(self, context: ChandasContext) -> ChandasResult:
        return self.strategy.analyze(context)

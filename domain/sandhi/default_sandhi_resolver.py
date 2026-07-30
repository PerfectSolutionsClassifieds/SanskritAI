from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Resolver

Canonical Sandhi resolver façade.

This implementation keeps the resolver thin and delegates all
Sandhi work to the configured SandhiStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)
from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)
from SanskritAI.domain.sandhi.sandhi_resolver import (
    SandhiResolver,
)
from SanskritAI.domain.sandhi.sandhi_strategy import (
    SandhiStrategy,
)


class DefaultSandhiResolver(
    SandhiResolver,
):
    """
    Default Sandhi resolver façade.
    """

    def __init__(
        self,
        strategy: SandhiStrategy | None = None,
    ) -> None:
        super().__init__(
            strategy=(
                strategy
                if strategy is not None
                else DefaultSandhiStrategy()
            )
        )

    @property
    def display_name(self) -> str:
        return "Default Sandhi Resolver"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Thin Sandhi resolver façade over the canonical "
            "Sandhi strategy."
        )

    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:
        """
        Resolves the supplied Sandhi context.
        """
        return self.strategy.resolve(context)

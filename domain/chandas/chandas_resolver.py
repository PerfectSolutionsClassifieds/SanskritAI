from __future__ import annotations

"""
SanskritAI
==========

Chandas Resolver

Defines the façade for Chandas resolution.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.chandas.chandas_context import ChandasContext
from SanskritAI.domain.chandas.chandas_result import ChandasResult
from SanskritAI.domain.chandas.chandas_strategy import ChandasStrategy


class ChandasResolver(
    Displayable,
):
    """
    Canonical façade for Chandas resolution.
    """

    def __init__(self, strategy: ChandasStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates Chandas analysis to a strategy."

    @property
    def strategy(self) -> ChandasStrategy:
        return self._strategy

    def analyze(self, context: ChandasContext) -> ChandasResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

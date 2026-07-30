from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Resolver

Defines the façade for Pratyaya resolution.

PratyayaResolver delegates all affix analysis work to a
configured PratyayaStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_result import PratyayaResult
from SanskritAI.domain.pratyaya.pratyaya_strategy import PratyayaStrategy


class PratyayaResolver(
    Displayable,
):
    """
    Canonical façade for Pratyaya resolution.
    """

    def __init__(self, strategy: PratyayaStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates Pratyaya analysis to a strategy."

    @property
    def strategy(self) -> PratyayaStrategy:
        return self._strategy

    def analyze(self, context: PratyayaContext) -> PratyayaResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

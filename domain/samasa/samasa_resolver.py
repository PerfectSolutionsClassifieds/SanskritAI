from __future__ import annotations

"""
SanskritAI
==========

Samasa Resolver

Defines the façade for Samasa resolution.

SamasaResolver delegates all compound analysis work to a
configured SamasaStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_result import SamasaResult
from SanskritAI.domain.samasa.samasa_strategy import SamasaStrategy


class SamasaResolver(
    Displayable,
):
    """
    Canonical façade for Samasa resolution.
    """

    def __init__(self, strategy: SamasaStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates Samasa analysis to a strategy."

    @property
    def strategy(self) -> SamasaStrategy:
        return self._strategy

    def analyze(self, context: SamasaContext) -> SamasaResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Dhatu Resolver

Defines the façade for Dhatu resolution.

DhatuResolver delegates all root analysis work to a configured
DhatuStrategy.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_result import DhatuResult
from SanskritAI.domain.dhatu.dhatu_strategy import DhatuStrategy


class DhatuResolver(
    Displayable,
):
    """
    Canonical façade for Dhatu resolution.
    """

    def __init__(self, strategy: DhatuStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates Dhatu analysis to a strategy."

    @property
    def strategy(self) -> DhatuStrategy:
        return self._strategy

    def analyze(self, context: DhatuContext) -> DhatuResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

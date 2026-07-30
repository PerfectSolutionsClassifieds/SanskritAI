from __future__ import annotations

"""
SanskritAI
==========

Alankara Resolver

Defines the façade for Alankara resolution.

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.alankara.alankara_context import AlankaraContext
from SanskritAI.domain.alankara.alankara_result import AlankaraResult
from SanskritAI.domain.alankara.alankara_strategy import AlankaraStrategy


class AlankaraResolver(
    Displayable,
):
    """
    Canonical façade for Alankara resolution.
    """

    def __init__(self, strategy: AlankaraStrategy) -> None:
        self._strategy = strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Delegates Alankara analysis to a strategy."

    @property
    def strategy(self) -> AlankaraStrategy:
        return self._strategy

    def analyze(self, context: AlankaraContext) -> AlankaraResult:
        return self.strategy.analyze(context)

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Strategy

Defines the abstract strategy for Pratyaya analysis.

A PratyayaStrategy encapsulates the algorithm responsible for
identifying affixes and returning a PratyayaResult.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_result import PratyayaResult


class PratyayaStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Pratyaya analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Pratyaya analysis strategy."

    @abstractmethod
    def analyze(self, context: PratyayaContext) -> PratyayaResult:
        """
        Analyzes the supplied Pratyaya context.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

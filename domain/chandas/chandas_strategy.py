from __future__ import annotations

"""
SanskritAI
==========

Chandas Strategy

Defines the abstract strategy for Chandas analysis.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.chandas.chandas_context import ChandasContext
from SanskritAI.domain.chandas.chandas_result import ChandasResult


class ChandasStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Chandas analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Chandas analysis strategy."

    @abstractmethod
    def analyze(self, context: ChandasContext) -> ChandasResult:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

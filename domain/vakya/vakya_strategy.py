from __future__ import annotations

"""
SanskritAI
==========

Vakya Strategy

Defines the abstract strategy for sentence-level analysis.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_result import VakyaResult


class VakyaStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Vakya analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Vakya analysis strategy."

    @abstractmethod
    def analyze(self, context: VakyaContext) -> VakyaResult:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

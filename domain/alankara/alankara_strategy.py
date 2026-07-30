from __future__ import annotations

"""
SanskritAI
==========

Alankara Strategy

Defines the abstract strategy for Alankara analysis.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.alankara.alankara_context import AlankaraContext
from SanskritAI.domain.alankara.alankara_result import AlankaraResult


class AlankaraStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Alankara analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Alankara analysis strategy."

    @abstractmethod
    def analyze(self, context: AlankaraContext) -> AlankaraResult:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

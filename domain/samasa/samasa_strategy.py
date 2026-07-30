from __future__ import annotations

"""
SanskritAI
==========

Samasa Strategy

Defines the abstract strategy for Samasa analysis.

A SamasaStrategy encapsulates the algorithm responsible for
analyzing compound forms and returning a SamasaResult.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_result import SamasaResult


class SamasaStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Samasa analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Samasa analysis strategy."

    @abstractmethod
    def analyze(self, context: SamasaContext) -> SamasaResult:
        """
        Analyzes the supplied Samasa context.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Dhatu Strategy

Defines the abstract strategy for Dhatu analysis.

A DhatuStrategy encapsulates the algorithm responsible for
identifying roots and returning a DhatuResult.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_result import DhatuResult


class DhatuStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Dhatu analysis strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Dhatu analysis strategy."

    @abstractmethod
    def analyze(self, context: DhatuContext) -> DhatuResult:
        """
        Analyzes the supplied Dhatu context.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

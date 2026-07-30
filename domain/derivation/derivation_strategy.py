from __future__ import annotations

"""
SanskritAI
==========

Derivation Strategy

Defines the abstract strategy for morphological derivation.

A DerivationStrategy encapsulates the algorithm responsible for
combining a Dhatu and a Pratyaya into a derived form and
returning a DerivationResult.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.derivation.derivation_context import DerivationContext
from SanskritAI.domain.derivation.derivation_result import DerivationResult


class DerivationStrategy(
    ABC,
    Displayable,
):
    """
    Abstract morphological derivation strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract derivation strategy."

    @abstractmethod
    def analyze(
        self,
        context: DerivationContext,
    ) -> DerivationResult:
        """
        Analyzes the supplied derivation context.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

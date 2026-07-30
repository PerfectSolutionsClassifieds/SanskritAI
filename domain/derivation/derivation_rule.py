from __future__ import annotations

"""
SanskritAI
==========

Derivation Rule

Defines the abstract foundation for every morphological
derivation rule.

A DerivationRule performs one atomic derivational operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable DerivationRuleSets.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)


class DerivationRule(
    ABC,
    Displayable,
):
    """
    Abstract derivation rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract derivation rule."

    @abstractmethod
    def applies_to(
        self,
        context: DerivationContext,
    ) -> bool:
        """
        Determines whether this rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        context: DerivationContext,
    ) -> tuple[Any, ...]:
        """
        Applies the derivation rule and returns candidate outputs.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

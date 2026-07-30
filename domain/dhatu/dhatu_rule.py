from __future__ import annotations

"""
SanskritAI
==========

Dhatu Rule

Defines the abstract foundation for every Dhatu rule.

A DhatuRule performs one atomic root-analysis operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable DhatuRuleSets.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext


class DhatuRule(
    ABC,
    Displayable,
):
    """
    Abstract Dhatu rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Dhatu rule."

    @abstractmethod
    def applies_to(
        self,
        context: DhatuContext,
    ) -> bool:
        """
        Determines whether this rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        context: DhatuContext,
    ) -> tuple[Any, ...]:
        """
        Applies the Dhatu rule and returns candidate outputs.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

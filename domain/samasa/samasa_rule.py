from __future__ import annotations

"""
SanskritAI
==========

Samasa Rule

Defines the abstract foundation for every Samasa rule.

A SamasaRule performs one atomic compound-analysis operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable SamasaRuleSets.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.samasa.samasa_context import SamasaContext


class SamasaRule(
    ABC,
    Displayable,
):
    """
    Abstract Samasa rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Samasa rule."

    @abstractmethod
    def applies_to(
        self,
        context: SamasaContext,
    ) -> bool:
        """
        Determines whether this rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        context: SamasaContext,
    ) -> tuple[Any, ...]:
        """
        Applies the Samasa rule and returns candidate outputs.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

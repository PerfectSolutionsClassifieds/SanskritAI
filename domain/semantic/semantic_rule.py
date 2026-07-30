from __future__ import annotations

"""
SanskritAI
==========

Semantic Rule

Defines the abstract foundation for semantic rules.

A SemanticRule performs one atomic meaning-analysis operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable SemanticRuleSets.

Version
-------
v1.1.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.semantic.semantic_context import SemanticContext


class SemanticRule(
    ABC,
    Displayable,
):
    """
    Abstract semantic rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract semantic rule."

    @abstractmethod
    def applies_to(self, context: SemanticContext) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, context: SemanticContext) -> tuple[Any, ...]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Grammar Rule

Defines the abstract foundation for Sanskrit grammar rules.

A GrammarRule evaluates a grammatical subject and may produce
one or more grammar-domain outputs such as roles, relations,
or features.

This class is intentionally generic so that future grammar
kernels can specialize it without changing the overall
architecture.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable


class GrammarRule(
    ABC,
    Displayable,
):
    """
    Abstract grammar rule.
    """

    @property
    def identifier(self) -> str:
        return self.__class__.__name__

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract grammar rule."

    @abstractmethod
    def applies_to(
        self,
        subject: Any,
    ) -> bool:
        """
        Determines whether this rule applies to the supplied
        subject.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        subject: Any,
    ) -> tuple[Any, ...]:
        """
        Applies this rule to the supplied subject and returns
        grammar-domain outputs.

        Concrete implementations may later return typed grammar
        analysis objects.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

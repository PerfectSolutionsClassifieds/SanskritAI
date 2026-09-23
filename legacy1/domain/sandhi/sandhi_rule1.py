from __future__ import annotations

"""
SanskritAI
==========

Sandhi Rule

Defines the abstract foundation for every Sandhi rule.

A SandhiRule performs one atomic Sandhi transformation or
analysis. Rules are intentionally independent and stateless,
allowing them to be composed into reusable SandhiRuleSets.

Future specializations
----------------------

• SvaraSandhiRule
• VyanjanaSandhiRule
• VisargaSandhiRule
• RecursiveSandhiRule

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)


class SandhiRule(
    ABC,
    Displayable,
):
    """
    Abstract Sandhi rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Abstract Sandhi rule."
        )

    @abstractmethod
    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:
        """
        Determines whether this rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        """
        Applies the Sandhi rule.

        Returns
        -------
        tuple[str, ...]
            Candidate Sandhi outputs.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

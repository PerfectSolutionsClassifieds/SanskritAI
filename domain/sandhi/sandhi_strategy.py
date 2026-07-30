from __future__ import annotations

"""
SanskritAI
==========

Sandhi Strategy

Defines the abstract strategy for Sandhi analysis.

A SandhiStrategy encapsulates the algorithm responsible for
splitting, joining, or otherwise resolving Sandhi expressions.

The strategy is intentionally independent of concrete Sandhi
rules so that different approaches (rule-based, statistical,
hybrid, AI-assisted) may coexist.

Hierarchy
---------

SandhiStrategy
        │
        ├── DefaultSandhiStrategy
        ├── RuleBasedSandhiStrategy
        ├── RecursiveSandhiStrategy
        └── AISandhiStrategy

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)


class SandhiStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Sandhi analysis strategy.
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
            "Abstract Sandhi analysis strategy."
        )

    @abstractmethod
    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:
        """
        Performs Sandhi resolution.

        Parameters
        ----------
        context:
            Sandhi context.

        Returns
        -------
        SandhiResult
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text

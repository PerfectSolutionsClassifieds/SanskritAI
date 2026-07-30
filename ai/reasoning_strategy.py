from __future__ import annotations

"""
SanskritAI
==========

Reasoning Strategy

Defines the abstract reasoning policy.

A ReasoningStrategy encapsulates *how* reasoning is
performed, while the Reasoner coordinates the overall
reasoning lifecycle.

Architecture
------------

ReasoningContext
        │
        ▼
ReasoningStrategy
        │
        ▼
Reasoner
"""

from abc import ABC, abstractmethod

from SanskritAI.ai.inference_result import InferenceResult
from SanskritAI.ai.reasoning_context import ReasoningContext
from SanskritAI.core.mixins.displayable import Displayable


class ReasoningStrategy(
    ABC,
    Displayable,
):
    """
    Abstract reasoning policy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract reasoning strategy."

    @abstractmethod
    def reason(
        self,
        context: ReasoningContext,
    ) -> InferenceResult:
        """
        Executes reasoning according to this strategy.
        """
        raise NotImplementedError

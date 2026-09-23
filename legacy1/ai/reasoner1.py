from __future__ import annotations

"""
SanskritAI
==========

Reasoner

Defines the abstract reasoning engine.

A Reasoner consumes a ReasoningContext and produces an
InferenceResult.

Concrete implementations may perform symbolic reasoning,
LLM-backed reasoning, hybrid reasoning, or domain-specific
reasoning.

Architecture
------------

ReasoningContext
        │
        ▼
Reasoner
        │
        ▼
InferenceResult

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.ai.inference_result import InferenceResult
from SanskritAI.ai.reasoning_context import ReasoningContext
from SanskritAI.core.mixins.displayable import Displayable


class Reasoner(
    ABC,
    Displayable,
):
    """
    Abstract reasoning engine.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract reasoning engine."

    @abstractmethod
    def reason(
        self,
        context: ReasoningContext,
    ) -> InferenceResult:
        """
        Performs reasoning over the supplied context.
        """
        raise NotImplementedError

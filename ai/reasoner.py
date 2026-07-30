from __future__ import annotations

"""
SanskritAI
==========

Reasoner

Coordinates reasoning by delegating to a
ReasoningStrategy.
"""

from abc import ABC, abstractmethod

from SanskritAI.ai.inference_result import InferenceResult
from SanskritAI.ai.reasoning_context import ReasoningContext
from SanskritAI.ai.reasoning_strategy import ReasoningStrategy
from SanskritAI.core.mixins.displayable import Displayable


class Reasoner(
    ABC,
    Displayable,
):
    """
    Abstract reasoning coordinator.
    """

    def __init__(
        self,
        strategy: ReasoningStrategy,
    ):
        self._strategy = strategy

    @property
    def strategy(self) -> ReasoningStrategy:
        return self._strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract reasoning coordinator."

    @abstractmethod
    def reason(
        self,
        context: ReasoningContext,
    ) -> InferenceResult:
        """
        Coordinates one reasoning session.
        """
        raise NotImplementedError

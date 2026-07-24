from __future__ import annotations

"""
SanskritAI

Abstract Orchestrator.

Coordinates execution.

Execution policy is delegated to an ExecutionStrategy.
"""

from abc import ABC, abstractmethod

from SanskritAI.application.execution_context import ExecutionContext
from SanskritAI.application.execution_plan import ExecutionPlan
from SanskritAI.application.execution_result import ExecutionResult
from SanskritAI.application.execution_strategy import ExecutionStrategy
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.mixins.displayable import Displayable


class Orchestrator(
    ABC,
    Displayable,
):
    """
    Coordinates execution.

    Never performs execution itself.
    """

    def __init__(
        self,
        strategy: ExecutionStrategy,
    ):
        self._strategy = strategy

    @property
    def strategy(self) -> ExecutionStrategy:
        return self._strategy

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract application orchestrator."

    @abstractmethod
    def create_context(
        self,
        runtime: RuntimeContext,
        plan: ExecutionPlan,
    ) -> ExecutionContext:
        ...

    @abstractmethod
    def orchestrate(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:
        ...

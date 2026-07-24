from __future__ import annotations

"""
SanskritAI
==========

Orchestrator

Defines the abstract execution engine responsible for
executing ExecutionPlans.

Concrete implementations execute Tasks, Workflows and
Pipelines while remaining completely independent of their
declarative definitions.

Architecture
------------

ExecutionPlan
        │
        ▼
ExecutionContext
        │
        ▼
ExecutionResult
        ▲
        │
   Orchestrator
        │
        ▼
DefaultOrchestrator

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.application.execution_context import ExecutionContext
from SanskritAI.application.execution_plan import ExecutionPlan
from SanskritAI.application.execution_result import ExecutionResult
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.mixins.displayable import Displayable


class Orchestrator(
    ABC,
    Displayable,
):
    """
    Abstract execution engine.

    An Orchestrator converts declarative application models
    into immutable execution results.
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
            "Abstract application execution engine."
        )

    @abstractmethod
    def create_context(
        self,
        runtime: RuntimeContext,
        plan: ExecutionPlan,
    ) -> ExecutionContext:
        """
        Creates an immutable execution context.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """
        Executes the supplied execution context.
        """
        raise NotImplementedError

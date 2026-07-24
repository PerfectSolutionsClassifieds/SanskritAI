from __future__ import annotations

"""
SanskritAI
==========

Execution Strategy

Defines the abstract execution policy responsible for
executing an ExecutionPlan.

An ExecutionStrategy determines *how* an execution plan
is carried out, while the Orchestrator coordinates the
overall execution lifecycle.

Concrete strategies may include:

- SequentialExecutionStrategy
- ParallelExecutionStrategy
- DistributedExecutionStrategy
- LazyExecutionStrategy
- AIExecutionStrategy

Architecture
------------

ExecutionPlan
        │
        ▼
ExecutionStrategy
        │
        ▼
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
from SanskritAI.application.execution_result import ExecutionResult
from SanskritAI.core.mixins.displayable import Displayable


class ExecutionStrategy(
    ABC,
    Displayable,
):
    """
    Abstract execution policy.

    An ExecutionStrategy defines *how* a prepared execution
    context is executed. It owns the execution policy but
    not the orchestration lifecycle.
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
            "Abstract execution strategy."
        )

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """
        Executes the supplied execution context according to
        this strategy.
        """
        raise NotImplementedError

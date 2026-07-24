from __future__ import annotations

"""
Default Orchestrator.

The canonical runtime coordinator.

Responsibilities

• create ExecutionContext

• delegate execution to ExecutionStrategy

• return ExecutionResult

Nothing more.
"""

from SanskritAI.application.execution_context import ExecutionContext
from SanskritAI.application.execution_plan import ExecutionPlan
from SanskritAI.application.execution_result import ExecutionResult
from SanskritAI.application.orchestrator import Orchestrator
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext


class DefaultOrchestrator(
    Orchestrator,
):
    """
    Canonical orchestrator implementation.
    """

    def create_context(
        self,
        runtime: RuntimeContext,
        plan: ExecutionPlan,
    ) -> ExecutionContext:

        return ExecutionContext(
            runtime=runtime,
            plan=plan,
        )

    def orchestrate(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:

        #
        # Future responsibilities:
        #
        # publish ExecutionStarted
        # diagnostics
        # timing
        # telemetry
        # metrics
        # tracing
        #

        return self.strategy.execute(context)

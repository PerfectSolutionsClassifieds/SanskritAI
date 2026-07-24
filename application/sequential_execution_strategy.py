from __future__ import annotations

"""
Sequential Execution Strategy.

Executes tasks sequentially.

This is the canonical execution strategy for SanskritAI v1.0.
"""

from SanskritAI.application.execution_context import ExecutionContext
from SanskritAI.application.execution_result import ExecutionResult
from SanskritAI.application.execution_strategy import ExecutionStrategy
from SanskritAI.application.task_result_collection import (
    TaskResultCollection,
)


class SequentialExecutionStrategy(
    ExecutionStrategy,
):
    """
    Sequential execution policy.
    """

    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:

        #
        # Real task execution will gradually be introduced
        # during AI layer implementation.
        #

        results = TaskResultCollection()

        return ExecutionResult(
            context=context,
            results=results,
            succeeded=True,
            message="Execution completed successfully.",
        )

from __future__ import annotations

"""
SanskritAI
==========

Core Pipeline Step

Represents one executable stage within the generic Pipeline
Framework.

A PipelineStep encapsulates exactly one operation while the
Pipeline orchestrates the execution of multiple steps.

The step itself remains completely domain-independent and
therefore may be reused by every SanskritAI kernel.

Hierarchy
---------

PipelineContext
        │
        ▼
PipelineStep
        │
        ▼
Pipeline
        │
        ▼
PipelineResult

Future
------

Later versions may additionally support

    • conditional execution
    • dependency graphs
    • retry policies
    • parallel execution
    • timing metrics
    • rule provenance
    • event hooks

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any, Callable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.value_objects.value_object import ValueObject


PipelineOperation = Callable[
    [PipelineContext, Any],
    Any,
]


@dataclass(frozen=True, slots=True)
class PipelineStep(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Generic executable pipeline step.
    """

    identifier: str

    name: str

    kernel: str

    operation: PipelineOperation

    priority: int = 100

    enabled: bool = True

    description: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return (
            f"{self.kernel} :: "
            f"{self.name}"
        )

    @property
    def display_description(self) -> str:
        return self.description

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
        previous_result: Any = None,
    ) -> Any:
        """
        Executes the pipeline step.
        """

        if not self.enabled:
            return previous_result

        return self.operation(
            context,
            previous_result,
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_disabled(self) -> bool:
        return not self.enabled

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "PipelineStep",
    ) -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return self.display_text

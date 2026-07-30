from __future__ import annotations

"""
SanskritAI
==========

Core Pipeline Trace

Provides a generic execution trace for the reusable Pipeline
Framework.

Every Pipeline execution produces a PipelineTrace that records
each executed PipelineStep together with its input, output,
execution status, and diagnostics.

Unlike the domain-specific DerivationPipelineTrace, this class
is completely kernel-independent and therefore reusable by
Derivation, Semantic, Vakya, Chandas, Alankara,
Knowledge Graph, and future kernels.

Hierarchy
---------

PipelineContext
        │
        ▼
PipelineStep
        │
        ▼
PipelineTraceEntry
        │
        ▼
PipelineTrace
        │
        ▼
PipelineResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.collections.collection import Collection
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.pipeline.pipeline_step import PipelineStep
from SanskritAI.core.value_objects.value_object import ValueObject


# ---------------------------------------------------------
# Trace Entry
# ---------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PipelineTraceEntry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable record describing one pipeline step execution.
    """

    step: PipelineStep

    input_value: Any = None

    output_value: Any = None

    succeeded: bool = True

    diagnostics: tuple[str, ...] = ()

    execution_order: int = 0

    confidence: float = 1.0

    # -----------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.step.identifier

    @property
    def display_name(self) -> str:
        return self.step.display_name

    @property
    def display_text(self) -> str:
        state = "Succeeded" if self.succeeded else "Failed"
        return (
            f"{self.step.display_name}"
            f" [{state}]"
        )

    @property
    def display_description(self) -> str:
        return self.step.display_description

    # -----------------------------------------------------

    @property
    def has_output(self) -> bool:
        return self.output_value is not None

    @property
    def has_input(self) -> bool:
        return self.input_value is not None

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    def __str__(self) -> str:
        return self.display_text


# ---------------------------------------------------------
# Trace Collection
# ---------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PipelineTrace(
    Collection[PipelineTraceEntry],
    Immutable,
    Displayable,
):
    """
    Immutable execution trace for a Pipeline.
    """

    items: tuple[
        PipelineTraceEntry,
        ...
    ] = field(default_factory=tuple)

    # -----------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Pipeline Trace"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.count} steps)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable execution history of a Pipeline."
        )

    # -----------------------------------------------------

    @property
    def first(self) -> PipelineTraceEntry | None:
        if not self.items:
            return None
        return self.items[0]

    @property
    def last(self) -> PipelineTraceEntry | None:
        if not self.items:
            return None
        return self.items[-1]

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    @property
    def successful_steps(self) -> tuple[
        PipelineTraceEntry,
        ...
    ]:
        return tuple(
            step
            for step in self.items
            if step.succeeded
        )

    @property
    def failed_steps(self) -> tuple[
        PipelineTraceEntry,
        ...
    ]:
        return tuple(
            step
            for step in self.items
            if not step.succeeded
        )

    @property
    def success_count(self) -> int:
        return len(self.successful_steps)

    @property
    def failure_count(self) -> int:
        return len(self.failed_steps)

    @property
    def succeeded(self) -> bool:
        return self.failure_count == 0

    # -----------------------------------------------------

    def add(
        self,
        entry: PipelineTraceEntry,
    ) -> "PipelineTrace":
        """
        Returns a new trace containing the additional entry.
        """
        return PipelineTrace(
            items=self.items + (entry,)
        )

    def __str__(self) -> str:
        return self.display_text

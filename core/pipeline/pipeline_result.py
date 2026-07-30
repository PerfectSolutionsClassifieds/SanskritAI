from __future__ import annotations

"""
SanskritAI
==========

Core Pipeline Result

Defines the generic immutable result produced by every
Pipeline execution.

Unlike domain-specific result objects, PipelineResult contains
only execution-level information and therefore can be reused
by every kernel within SanskritAI.

Hierarchy
---------

PipelineContext
        │
        ▼
PipelineStep
        │
        ▼
PipelineTrace
        │
        ▼
PipelineResult

Future
------

Later versions may additionally include

    • execution duration
    • memory statistics
    • pipeline metrics
    • execution provenance
    • event history
    • nested pipelines

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_trace import PipelineTrace
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PipelineResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by a Pipeline.
    """

    context: PipelineContext

    trace: PipelineTrace

    output: Any = None

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[str, ...] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.context.identifier

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Pipeline Result"

    @property
    def display_text(self) -> str:
        state = (
            "Succeeded"
            if self.succeeded
            else "Failed"
        )
        return (
            f"{self.display_name}"
            f" [{state}]"
        )

    @property
    def display_description(self) -> str:
        if self.has_diagnostics:
            return self.diagnostics[0]
        return ""

    # ---------------------------------------------------------
    # Context shortcuts
    # ---------------------------------------------------------

    @property
    def subject(self):
        return self.context.subject

    @property
    def metadata(self):
        return self.context.metadata

    @property
    def source(self) -> str:
        return self.context.source

    @property
    def language(self) -> str:
        return self.context.language

    @property
    def script(self) -> str:
        return self.context.script

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    @property
    def has_output(self) -> bool:
        return self.output is not None

    @property
    def result(self):
        """
        Compatibility alias.
        """
        return self.output

    @property
    def resolved(self) -> bool:
        return (
            self.succeeded
            and self.has_output
        )

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    # ---------------------------------------------------------
    # Confidence
    # ---------------------------------------------------------

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    @property
    def is_uncertain(self) -> bool:
        return not self.is_confident

    # ---------------------------------------------------------
    # Trace
    # ---------------------------------------------------------

    @property
    def has_trace(self) -> bool:
        return self.trace.is_not_empty

    @property
    def step_count(self) -> int:
        return self.trace.count

    @property
    def successful_steps(self) -> int:
        return self.trace.success_count

    @property
    def failed_steps(self) -> int:
        return self.trace.failure_count

    @property
    def first_step(self):
        return self.trace.first

    @property
    def last_step(self):
        return self.trace.last

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def first_diagnostic(self) -> str | None:
        if not self.diagnostics:
            return None
        return self.diagnostics[0]

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

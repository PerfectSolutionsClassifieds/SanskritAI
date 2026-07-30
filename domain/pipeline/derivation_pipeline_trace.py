from __future__ import annotations

"""
SanskritAI
==========

Derivation Pipeline Trace

Represents the immutable execution history of the Morphological
Derivation Pipeline.

Every pipeline execution produces a trace consisting of one
TraceEntry for every executed pipeline step.

This becomes the canonical derivation debugger for SanskritAI,
allowing every transformation from Dhātu through Knowledge
Graph construction to be inspected.

Hierarchy
---------

Pipeline Context
        │
        ▼
Pipeline Step
        │
        ▼
Pipeline TraceEntry
        │
        ▼
Pipeline Trace
        │
        ▼
Pipeline Result

Future
------

Later versions may additionally capture

    • execution duration
    • applied Pāṇinian rules
    • diagnostics
    • rollback information
    • provenance
    • explanation chain
    • visualization

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.pipeline.derivation_pipeline_step import (
    DerivationPipelineStep,
)


# ---------------------------------------------------------
# Trace Entry
# ---------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DerivationPipelineTraceEntry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One execution record inside the pipeline trace.
    """

    step: DerivationPipelineStep

    input_value: Any = None

    output_value: Any = None

    succeeded: bool = True

    diagnostics: tuple[str, ...] = field(
        default_factory=tuple,
    )

    duration_ms: float | None = None

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
        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:
        return self.step.display_description

    @property
    def has_input(self) -> bool:
        return self.input_value is not None

    @property
    def has_output(self) -> bool:
        return self.output_value is not None

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def kernel(self) -> str:
        return self.step.kernel


# ---------------------------------------------------------
# Pipeline Trace
# ---------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DerivationPipelineTrace(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution history of an entire derivation
    pipeline.
    """

    entries: tuple[
        DerivationPipelineTraceEntry,
        ...
    ] = ()

    # -----------------------------------------------------

    @property
    def identifier(self) -> str:
        return "pipeline.trace"

    @property
    def display_name(self) -> str:
        return "Derivation Pipeline Trace"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name} "
            f"({self.count} steps)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Execution history of the Morphological "
            "Derivation Pipeline."
        )

    # -----------------------------------------------------
    # Collection helpers
    # -----------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.entries)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    @property
    def first(
        self,
    ) -> DerivationPipelineTraceEntry | None:
        if self.is_empty:
            return None
        return self.entries[0]

    @property
    def last(
        self,
    ) -> DerivationPipelineTraceEntry | None:
        if self.is_empty:
            return None
        return self.entries[-1]

    @property
    def successful_steps(self) -> int:
        return sum(
            entry.succeeded
            for entry in self.entries
        )

    @property
    def failed_steps(self) -> int:
        return self.count - self.successful_steps

    @property
    def has_failures(self) -> bool:
        return self.failed_steps > 0

    @property
    def kernels(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            entry.kernel
            for entry in self.entries
        )

    # -----------------------------------------------------
    # Immutable modifiers
    # -----------------------------------------------------

    def add(
        self,
        entry: DerivationPipelineTraceEntry,
    ) -> "DerivationPipelineTrace":
        """
        Returns a new trace with one additional execution
        record.
        """
        return DerivationPipelineTrace(
            entries=self.entries + (entry,),
        )

    def extend(
        self,
        entries: tuple[
            DerivationPipelineTraceEntry,
            ...,
        ],
    ) -> "DerivationPipelineTrace":
        return DerivationPipelineTrace(
            entries=self.entries + entries,
        )

    # -----------------------------------------------------
    # Queries
    # -----------------------------------------------------

    def by_kernel(
        self,
        kernel: str,
    ) -> tuple[
        DerivationPipelineTraceEntry,
        ...,
    ]:
        return tuple(
            entry
            for entry in self.entries
            if entry.kernel == kernel
        )

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return self.count

    def __str__(self) -> str:
        return self.display_text

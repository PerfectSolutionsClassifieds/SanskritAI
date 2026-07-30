from __future__ import annotations

"""
SanskritAI
==========

Derivation Pipeline Result

Top-level immutable result produced by the Morphological
Derivation Pipeline.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.pipeline.derivation_pipeline_context import (
    DerivationPipelineContext,
)
from SanskritAI.domain.pipeline.derivation_pipeline_trace import (
    DerivationPipelineTrace,
)


@dataclass(frozen=True, slots=True)
class DerivationPipelineResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result returned by the Morphological
    Derivation Pipeline.
    """

    context: DerivationPipelineContext

    value: Any = None

    trace: DerivationPipelineTrace = field(
        default_factory=DerivationPipelineTrace,
    )

    diagnostics: tuple[str, ...] = ()

    succeeded: bool = True

    confidence: float = 1.0

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def display_name(self) -> str:
        return "Derivation Pipeline Result"

    @property
    def display_text(self) -> str:
        state = "Succeeded" if self.succeeded else "Failed"
        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:
        return (
            "Immutable result of the Morphological "
            "Derivation Pipeline."
        )

    @property
    def resolved(self) -> bool:
        return self.succeeded and self.value is not None

    @property
    def has_trace(self) -> bool:
        return self.trace.is_not_empty

    @property
    def trace_step_count(self) -> int:
        return self.trace.count

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def result(self):
        return self.value

    def __str__(self) -> str:
        return self.display_text

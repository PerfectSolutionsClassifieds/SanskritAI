from __future__ import annotations

"""
SanskritAI
==========

Derivation Pipeline Step

Represents one executable stage of the Morphological
Derivation Pipeline.

The pipeline itself is intentionally generic. Every linguistic
kernel (Dhātu, Pratyaya, Paninian Rule Engine, Derivation,
Sandhi, Samāsa, Grammar, Semantics, Chandas, Alaṅkāra,
Vākya, Knowledge Graph, etc.) participates by implementing
one or more pipeline steps.

Hierarchy
---------

Pipeline Context
        │
        ▼
Pipeline Step
        │
        ▼
Pipeline Trace
        │
        ▼
Pipeline Result

Future
------

Later versions may support

• conditional execution
• priorities
• dependencies
• rollback
• retry
• parallel execution
• asynchronous kernels
• rule tracing
• profiling

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Callable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.pipeline.derivation_pipeline_context import (
    DerivationPipelineContext,
)


PipelineCallable = Callable[
    [DerivationPipelineContext, Any],
    Any,
]


@dataclass(frozen=True, slots=True)
class DerivationPipelineStep(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One executable stage of the Morphological Derivation
    Pipeline.
    """

    identifier: str

    name: str

    kernel: str

    operation: PipelineCallable

    description: str = ""

    priority: int = 100

    enabled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return f"{self.kernel} :: {self.name}"

    @property
    def display_description(self) -> str:
        return self.description

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: DerivationPipelineContext,
        value: Any,
    ) -> Any:
        """
        Executes this pipeline step.

        Parameters
        ----------
        context
            Pipeline execution context.

        value
            Current pipeline object produced by the previous
            step.

        Returns
        -------
        Any
            Output produced by this step.
        """
        return self.operation(
            context,
            value,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_disabled(self) -> bool:
        return not self.enabled

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.metadata.get(
            key,
            default,
        )

    def with_priority(
        self,
        priority: int,
    ) -> "DerivationPipelineStep":
        """
        Returns an immutable copy with updated priority.
        """
        return DerivationPipelineStep(
            identifier=self.identifier,
            name=self.name,
            kernel=self.kernel,
            operation=self.operation,
            description=self.description,
            priority=priority,
            enabled=self.enabled,
            metadata=dict(self.metadata),
        )

    def with_enabled(
        self,
        enabled: bool,
    ) -> "DerivationPipelineStep":
        """
        Returns an immutable copy with updated enabled flag.
        """
        return DerivationPipelineStep(
            identifier=self.identifier,
            name=self.name,
            kernel=self.kernel,
            operation=self.operation,
            description=self.description,
            priority=self.priority,
            enabled=enabled,
            metadata=dict(self.metadata),
        )

    def __lt__(
        self,
        other: "DerivationPipelineStep",
    ) -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return self.display_text

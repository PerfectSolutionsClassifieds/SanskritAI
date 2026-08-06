from __future__ import annotations

"""
SanskritAI
==========

Resolution State

Internal orchestration state used by the Resolution Pipeline.

ResolutionState is the shared object that flows through every
ResolutionStage. Each stage enriches this object with its own
resolution result while preserving previously computed results.

This object is intentionally mutable during pipeline execution.
The immutable public API remains ResolutionResult.

Relationship
------------

ResolutionContext
        │
        ▼
ResolutionState
        │
        ├── LexicalResolutionResult
        ├── MorphologicalResolutionResult
        ├── SandhiResolutionResult
        ├── SamasaResolutionResult
        ├── SemanticResolutionResult
        │
        ▼
ResolutionPipeline

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)

# Domain-specific results

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.sandhi.sandhi_resolution_result import (
    SandhiResolutionResult,
)

from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)


@dataclass(slots=True)
class ResolutionState:
    """
    Mutable orchestration state shared by every ResolutionStage.
    """

    context: ResolutionContext

    # ---------------------------------------------------------
    # Stage results
    # ---------------------------------------------------------

    lexical_result: (
        LexicalResolutionResult | None
    ) = None

    morphological_result: (
        MorphologicalResolutionResult | None
    ) = None

    sandhi_result: (
        SandhiResolutionResult | None
    ) = None

    samasa_result: (
        SamasaResolutionResult | None
    ) = None

    semantic_result: (
        SemanticResolutionResult | None
    ) = None

    # ---------------------------------------------------------
    # Pipeline metadata
    # ---------------------------------------------------------

    payload: Any = None

    confidence: float = 1.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    diagnostics: list[
        ResolutionDiagnostic
    ] = field(
        default_factory=list,
    )

    completed_stages: list[str] = field(
        default_factory=list,
    )

    failed_stage: str | None = None

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def subject(self) -> Any:
        return self.context.subject

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def has_lexical(self) -> bool:
        return self.lexical_result is not None

    @property
    def has_morphology(self) -> bool:
        return self.morphological_result is not None

    @property
    def has_sandhi(self) -> bool:
        return self.sandhi_result is not None

    @property
    def has_samasa(self) -> bool:
        return self.samasa_result is not None

    @property
    def has_semantics(self) -> bool:
        return self.semantic_result is not None

    @property
    def stage_count(self) -> int:
        return len(self.completed_stages)

    @property
    def has_failures(self) -> bool:
        return self.failed_stage is not None

    @property
    def succeeded(self) -> bool:
        return not self.has_failures

    # ---------------------------------------------------------
    # Mutation helpers
    # ---------------------------------------------------------

    def mark_completed(
        self,
        stage_name: str,
    ) -> None:
        self.completed_stages.append(stage_name)

    def mark_failed(
        self,
        stage_name: str,
    ) -> None:
        self.failed_stage = stage_name

    def add_diagnostic(
        self,
        diagnostic: ResolutionDiagnostic,
    ) -> None:
        self.diagnostics.append(diagnostic)

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.metadata.get(
            key,
            default,
        )

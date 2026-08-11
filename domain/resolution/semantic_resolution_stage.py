from __future__ import annotations

"""
SanskritAI
==========

Semantic Resolution Stage

Pipeline stage responsible for semantic resolution.

This stage delegates semantic interpretation to the configured
SemanticService and returns a SemanticResolutionResult.

Pipeline
--------

ResolutionContext
        │
        ▼
SemanticResolutionStage
        │
        ▼
SemanticService
        │
        ▼
SemanticResolutionResult

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)
from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)
from SanskritAI.domain.semantic.semantic_service import (
    SemanticService,
)


@dataclass(frozen=True, slots=True)
class SemanticResolutionStage(
    ResolutionStage,
):
    """
    Canonical semantic pipeline stage.
    """

    service: SemanticService

    @property
    def name(self) -> str:
        return "Semantic"

    @property
    def display_name(self) -> str:
        return "Semantic Resolution Stage"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Pipeline stage responsible for canonical "
            "semantic resolution."
        )

    def execute(
        self,
        context: ResolutionContext,
    ) -> SemanticResolutionResult:
        """
        Executes semantic resolution.
        """
        return self.service.resolve(
            context,
        )

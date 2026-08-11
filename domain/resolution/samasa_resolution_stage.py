from __future__ import annotations

"""
SanskritAI
==========

Samasa Resolution Stage

Pipeline stage responsible for Samāsa resolution.

This stage delegates compound-word analysis to the configured
SamasaService and returns a SamasaResolutionResult.

Pipeline
--------

ResolutionContext
        │
        ▼
SamasaResolutionStage
        │
        ▼
SamasaService
        │
        ▼
SamasaResolutionResult

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

from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)
from SanskritAI.domain.samasa.samasa_service import (
    SamasaService,
)


@dataclass(frozen=True, slots=True)
class SamasaResolutionStage(
    ResolutionStage,
):
    """
    Canonical Samāsa pipeline stage.
    """

    service: SamasaService

    @property
    def name(self) -> str:
        return "Samasa"

    @property
    def display_name(self) -> str:
        return "Samasa Resolution Stage"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Pipeline stage responsible for canonical "
            "Samāsa resolution."
        )

    def execute(
        self,
        context: ResolutionContext,
    ) -> SamasaResolutionResult:
        """
        Executes Samāsa resolution.
        """
        return self.service.resolve(
            context,
        )

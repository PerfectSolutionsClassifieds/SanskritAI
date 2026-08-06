from __future__ import annotations

"""
SanskritAI
==========

Sandhi Resolution Stage

Pipeline stage responsible for Sandhi resolution.

The stage delegates Sandhi analysis to the configured
SandhiService and returns a SandhiResolutionResult.

Pipeline
--------

ResolutionContext
        │
        ▼
SandhiResolutionStage
        │
        ▼
SandhiService
        │
        ▼
SandhiResolutionResult

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

from SanskritAI.domain.sandhi.sandhi_resolution_result import (
    SandhiResolutionResult,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)


@dataclass(frozen=True, slots=True)
class SandhiResolutionStage(
    ResolutionStage,
):
    """
    Canonical Sandhi pipeline stage.
    """

    service: SandhiService

    @property
    def name(self) -> str:
        return "Sandhi"

    @property
    def display_name(self) -> str:
        return "Sandhi Resolution Stage"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Pipeline stage responsible for canonical "
            "Sandhi resolution."
        )

    def execute(
        self,
        context: ResolutionContext,
    ) -> SandhiResolutionResult:
        """
        Executes Sandhi resolution.
        """
        return self.service.resolve(
            context,
        )

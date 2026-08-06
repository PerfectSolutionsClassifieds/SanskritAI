from __future__ import annotations

"""
SanskritAI
==========

Morphology Resolution Stage

Pipeline stage responsible for morphological resolution.

The stage delegates morphological analysis to the configured
MorphologicalService and returns a MorphologicalResolutionResult.

Pipeline
--------

ResolutionContext
        │
        ▼
MorphologyResolutionStage
        │
        ▼
MorphologicalService
        │
        ▼
MorphologicalResolutionResult

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_service import (
    MorphologicalService,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


@dataclass(frozen=True, slots=True)
class MorphologyResolutionStage(
    ResolutionStage,
):
    """
    Canonical morphology pipeline stage.
    """

    service: MorphologicalService

    @property
    def name(self) -> str:
        return "Morphology"

    @property
    def display_name(self) -> str:
        return "Morphology Resolution Stage"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Pipeline stage responsible for canonical "
            "morphological resolution."
        )

    def execute(
        self,
        context: ResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Executes morphological resolution.
        """
        return self.service.resolve(context)

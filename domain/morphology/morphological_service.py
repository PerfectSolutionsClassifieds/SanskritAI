from __future__ import annotations

"""
SanskritAI
==========

Morphological Service

Application-facing façade for the Morphology Kernel.

The MorphologicalService is the canonical contributor for
morphological analysis within the Resolution Pipeline.

Architecture
------------

ResolutionPipeline
        │
        ▼
MorphologicalService
        │
        ▼
MorphologicalRepository
        │
        ▼
CanonicalKnowledgeRepository

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.morphology.morphological_repository import (
    MorphologicalRepository,
)

from SanskritAI.domain.morphology.default_morphological_resolution_kernel import (
    DefaultMorphologicalResolutionKernel,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MorphologicalService(
    ResolutionContributor,
    Displayable,
):
    """
    Domain façade for canonical morphology.

    Also serves as the Morphology contributor of the
    Resolution Pipeline.
    """

    repository: MorphologicalRepository

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Morphological Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Domain façade for canonical Sanskrit "
            "morphological analysis."
        )

    # ---------------------------------------------------------
    # Resolution Kernel
    # ---------------------------------------------------------

    @property
    def resolution_kernel(
        self,
    ) -> DefaultMorphologicalResolutionKernel:
        """
        Canonical morphology kernel.
        """
        return DefaultMorphologicalResolutionKernel(
            repository=self.repository,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Performs canonical morphological resolution.
        """
        return self.resolution_kernel.resolve(
            context,
        )

    # ---------------------------------------------------------
    # Pipeline Contribution
    # ---------------------------------------------------------

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Enriches the aggregate ResolutionResult with
        morphological analysis.
        """
        morphology_result = self.resolve(
            context,
        )

        return aggregate.with_morphology(
            morphology_result,
        )

    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return self.repository.count

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

from __future__ import annotations

"""
SanskritAI
==========

Semantic Service

Application-facing façade for the Semantic Kernel.

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)
from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)
from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.semantic.semantic_repository import (
    SemanticRepository,
)
from SanskritAI.domain.semantic.default_semantic_resolution_kernel import (
    DefaultSemanticResolutionKernel,
)
from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)


@dataclass(frozen=True, slots=True)
class SemanticService(
    ResolutionContributor,
    Displayable,
):
    repository: SemanticRepository

    @property
    def display_name(self) -> str:
        return "Semantic Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical Semantic service."

    @property
    def resolution_kernel(
        self,
    ) -> DefaultSemanticResolutionKernel:
        return DefaultSemanticResolutionKernel(
            repository=self.repository,
        )

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SemanticResolutionResult:
        return self.resolution_kernel.resolve(
            context,
        )

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:
        result = self.resolve(context)
        return aggregate.with_semantic(result)

    @property
    def count(self) -> int:
        return self.repository.count

    def __str__(self) -> str:
        return self.display_text

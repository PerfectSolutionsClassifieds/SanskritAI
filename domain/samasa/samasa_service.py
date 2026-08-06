from __future__ import annotations

"""
SanskritAI
==========

Samasa Service

Application-facing façade for the Samāsa Kernel.

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

from SanskritAI.domain.samasa.samasa_repository import (
    SamasaRepository,
)
from SanskritAI.domain.samasa.default_samasa_resolution_kernel import (
    DefaultSamasaResolutionKernel,
)
from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)


@dataclass(frozen=True, slots=True)
class SamasaService(
    ResolutionContributor,
    Displayable,
):
    repository: SamasaRepository

    @property
    def display_name(self) -> str:
        return "Samasa Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical Samāsa service."

    @property
    def resolution_kernel(
        self,
    ) -> DefaultSamasaResolutionKernel:
        return DefaultSamasaResolutionKernel(
            repository=self.repository,
        )

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SamasaResolutionResult:
        return self.resolution_kernel.resolve(
            context,
        )

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:
        result = self.resolve(context)
        return aggregate.with_samasa(result)

    @property
    def count(self) -> int:
        return self.repository.count

    def __str__(self) -> str:
        return self.display_text

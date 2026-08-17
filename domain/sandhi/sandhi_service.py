
from __future__ import annotations

"""
SanskritAI
==========

Sandhi Service

Application-facing façade for the Sandhi Resolution Kernel.

Architecture
------------

ResolutionContext
        │
        ▼
SandhiService
        │
        ▼
DefaultSandhiResolutionKernel
        │
        ▼
SandhiResolutionKernel
        │
        ▼
SandhiStrategy
        │
        ▼
SandhiResult

Version
-------
v3.1.0
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

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.default_sandhi_resolution_kernel import (
    DefaultSandhiResolutionKernel,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SandhiService(
    ResolutionContributor,
    Displayable,
):
    """
    Canonical application-facing Sandhi service.

    The service owns the concrete repository/kernel composition
    boundary while delegating actual Sandhi resolution to the
    kernel.
    """

    repository: SandhiRepository

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Sandhi Service"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return "Canonical Sandhi resolution service."

    # ---------------------------------------------------------
    # Kernel
    # ---------------------------------------------------------

    @property
    def resolution_kernel(
        self,
    ) -> DefaultSandhiResolutionKernel:

        return DefaultSandhiResolutionKernel(
            repository=self.repository,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SandhiResult:

        return self.resolution_kernel.resolve(
            context,
        )

    # ---------------------------------------------------------
    # Resolution Contribution
    # ---------------------------------------------------------

    def contribute(
        self,
        aggregate: ResolutionResult,
    ) -> ResolutionResult:

        return aggregate

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text

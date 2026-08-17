from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Resolution Kernel

Concrete Semantic kernel used by SemanticService.

The class owns repository composition while delegating semantic
orchestration to SemanticResolutionKernel.

Architecture
------------

SemanticService
        │
        ▼
DefaultSemanticResolutionKernel
        │
        ├── SemanticRepository
        │
        ▼
SemanticResolutionKernel
        │
        ▼
DefaultSemanticStrategy
        │
        ▼
SemanticResult
        │
        ▼
SemanticResolutionResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.semantic.default_semantic_strategy import (
    DefaultSemanticStrategy,
)

from SanskritAI.domain.semantic.semantic_context import (
    SemanticContext,
)

from SanskritAI.domain.semantic.semantic_repository import (
    SemanticRepository,
)

from SanskritAI.domain.semantic.semantic_resolution_kernel import (
    SemanticResolutionKernel,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)

from SanskritAI.domain.semantic.semantic_strategy import (
    SemanticStrategy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultSemanticResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Concrete Semantic Resolution Kernel.

    Repository ownership remains here, while linguistic
    orchestration remains in SemanticResolutionKernel.
    """

    repository: SemanticRepository

    strategy: SemanticStrategy = field(
        default_factory=DefaultSemanticStrategy,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Default Semantic Resolution Kernel"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Default concrete Semantic Resolution Kernel "
            "composed with a SemanticRepository."
        )

    # ---------------------------------------------------------
    # Strategy
    # ---------------------------------------------------------

    @property
    def resolution_strategy(
        self,
    ) -> SemanticStrategy:

        return self.strategy

    # ---------------------------------------------------------
    # Generic kernel
    # ---------------------------------------------------------

    @property
    def kernel(
        self,
    ) -> SemanticResolutionKernel:

        return SemanticResolutionKernel(
            strategy=self.strategy,
        )

    # ---------------------------------------------------------
    # Context adaptation
    # ---------------------------------------------------------

    def build_context(
        self,
        context: ResolutionContext,
    ) -> SemanticContext:
        """
        Adapt the orchestration-level ResolutionContext into
        SemanticContext.

        Existing metadata is preserved.
        """

        metadata = dict(
            getattr(
                context,
                "metadata",
                {},
            )
            or {}
        )

        return SemanticContext(
            identifier=context.identifier,
            subject=context.subject,
            source=context.source,
            language=context.language,
            script=context.script,
            allow_multiple_analyses=metadata.get(
                "allow_multiple_analyses",
                True,
            ),
            enable_recursive_analysis=metadata.get(
                "enable_recursive_analysis",
                True,
            ),
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SemanticResolutionResult:
        """
        Resolve an orchestration-level ResolutionContext.
        """

        semantic_context = self.build_context(
            context,
        )

        return self.kernel.resolve(
            semantic_context,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: ResolutionContext,
    ) -> SemanticResolutionResult:

        return self.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text

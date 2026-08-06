from __future__ import annotations

"""
SanskritAI
==========

Reader Engine

High-level entry point for the Reader Domain.

The ReaderEngine orchestrates the complete SanskritAI
linguistic pipeline.

Pipeline

ReaderContext
      │
      ▼
ResolutionPipeline
      │
      ▼
ResolutionResult
      │
      ▼
ReaderResult

The ReaderEngine intentionally contains no linguistic
analysis logic.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
)

from SanskritAI.domain.reader.reader_context import (
    ReaderContext,
)

from SanskritAI.domain.reader.reader_result import (
    ReaderResult,
)

from SanskritAI.domain.resolution.default_resolution_pipeline import (
    default_resolution_pipeline,
)

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


@dataclass(slots=True)
class ReaderEngine(
    Displayable,
):
    """
    High-level orchestration engine.

    Responsible only for coordinating the linguistic
    pipeline.
    """

    knowledge_repository: CanonicalKnowledgeRepository = field(
        default_factory=CanonicalKnowledgeRepository,
    )

    pipeline: ResolutionPipeline | None = None

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:

        if self.pipeline is None:

            self.pipeline = default_resolution_pipeline(
                self.services,
            )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Reader Engine"

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
            "High-level SanskritAI reader engine."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def services(
        self,
    ) -> KnowledgeServiceRegistry:
        return self.knowledge_repository.services

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        reader_context: ReaderContext,
    ) -> ReaderResult:
        """
        Executes the complete linguistic pipeline.
        """

        resolution_context = ResolutionContext(
            identifier=reader_context.identifier,
            subject=reader_context.subject,
            source=reader_context.source,
            language=reader_context.language,
            script=reader_context.script,
            metadata=reader_context.metadata,
        )

        resolution_result = self.pipeline.execute(
            resolution_context,
        )

        return ReaderResult(
            context=reader_context,
            resolution=resolution_result,
        )

    # ---------------------------------------------------------
    # Future convenience methods
    # ---------------------------------------------------------

    def analyze_word(
        self,
        reader_context: ReaderContext,
    ) -> ReaderResult:
        return self.analyze(
            reader_context,
        )

    def analyze_sloka(
        self,
        reader_context: ReaderContext,
    ) -> ReaderResult:
        return self.analyze(
            reader_context,
        )

    def analyze_chapter(
        self,
        reader_context: ReaderContext,
    ) -> ReaderResult:
        return self.analyze(
            reader_context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text

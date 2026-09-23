from __future__ import annotations

"""
SanskritAI
==========

Reader Engine

High-level orchestration engine for SanskritAI.

ReaderEngine is the primary entry point for Phase-J
(Reader-Oriented Sanskrit Reference System).

Pipeline

ReaderContext
      │
      ▼
ResolutionPipeline
      │
      ▼
ReaderResult

Future versions may additionally orchestrate

    • Pragmatics

    • Commentarial reasoning

    • Cross-reference expansion

    • Canonical source citation

    • Knowledge graph traversal

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.reader.reader_context import (
    ReaderContext,
)

from SanskritAI.domain.reader.reader_result import (
    ReaderResult,
)

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)


@dataclass(slots=True)
class ReaderEngine(
    Displayable,
):
    """
    High-level Sanskrit reader engine.
    """

    pipeline: ResolutionPipeline

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Engine"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "High-level orchestration engine for the "
            "SanskritAI Reader System."
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def analyze(
        self,
        context: ReaderContext,
    ) -> ReaderResult:
        """
        Executes the complete linguistic pipeline.
        """

        resolution_result = self.pipeline.execute(context)

        return ReaderResult(
            context=context,

            lexical=resolution_result.lexical,

            morphology=resolution_result.morphology,

            sandhi=resolution_result.sandhi,

            samasa=resolution_result.samasa,

            semantic=resolution_result.semantic,

            metadata={
                "pipeline": self.pipeline.display_name,
            },
        )

    # ---------------------------------------------------------

    def analyze_word(
        self,
        context: ReaderContext,
    ) -> ReaderResult:
        """
        Alias for analyze().
        """

        return self.analyze(context)

    def analyze_token(
        self,
        context: ReaderContext,
    ) -> ReaderResult:
        """
        Alias for analyze().
        """

        return self.analyze(context)

    def analyze_expression(
        self,
        context: ReaderContext,
    ) -> ReaderResult:
        """
        Alias for analyze().
        """

        return self.analyze(context)

    def analyze_sloka(
        self,
        context: ReaderContext,
    ) -> ReaderResult:
        """
        Primary Reader API.

        Future versions will analyze an entire śloka by
        tokenizing it and invoking the Resolution Pipeline
        for each token before performing higher-level
        linguistic aggregation.
        """

        return self.analyze(context)

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

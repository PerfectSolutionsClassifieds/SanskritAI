from __future__ import annotations

"""
SanskritAI
==========

Lexical Resolution Stage

Pipeline stage responsible for lexical resolution.

The stage delegates lexical analysis to the configured
LexicalService and returns a LexicalResolutionResult.

Pipeline
--------

ResolutionContext
        │
        ▼
LexicalResolutionStage
        │
        ▼
LexicalService
        │
        ▼
LexicalResolutionResult

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


@dataclass(frozen=True, slots=True)
class LexicalResolutionStage(
    ResolutionStage,
):
    """
    Canonical lexical pipeline stage.
    """

    service: LexicalService

    @property
    def name(self) -> str:
        return "Lexical"

    @property
    def display_name(self) -> str:
        return "Lexical Resolution Stage"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Pipeline stage responsible for canonical "
            "lexical resolution."
        )

    def execute(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Executes lexical resolution.
        """
        return self.service.resolve(context)

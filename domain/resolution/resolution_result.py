from __future__ import annotations

"""
SanskritAI
==========

Resolution Result

Canonical aggregate representing the complete linguistic
resolution of a Sanskrit object.

Every ResolutionStage enriches this object.

Pipeline

Lexical
    ↓
Morphology
    ↓
Sandhi
    ↓
Samāsa
    ↓
Semantic
    ↓
Future:
    Pragmatics
    Commentary
    AI Reasoning

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.sandhi.sandhi_resolution_result import (
    SandhiResolutionResult,
)

from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)


@dataclass(frozen=True, slots=True)
class ResolutionResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Aggregate linguistic resolution.

    This object is progressively enriched by the
    ResolutionPipeline.
    """

    context: ResolutionContext

    lexical: LexicalResolutionResult | None = None

    morphology: MorphologicalResolutionResult | None = None

    sandhi: SandhiResolutionResult | None = None

    samasa: SamasaResolutionResult | None = None

    semantic: SemanticResolutionResult | None = None

    diagnostics: tuple[
        ResolutionDiagnostic,
        ...
    ] = field(default_factory=tuple)

    confidence: float = 0.0

    succeeded: bool = True

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Resolution Result"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Aggregate linguistic resolution."
        )

    # ---------------------------------------------------------
    # Subject
    # ---------------------------------------------------------

    @property
    def subject(self):
        return self.context.subject

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_lexical(self) -> bool:
        return self.lexical is not None

    @property
    def has_morphology(self) -> bool:
        return self.morphology is not None

    @property
    def has_sandhi(self) -> bool:
        return self.sandhi is not None

    @property
    def has_samasa(self) -> bool:
        return self.samasa is not None

    @property
    def has_semantic(self) -> bool:
        return self.semantic is not None

    @property
    def fully_resolved(self) -> bool:
        return (
            self.has_lexical
            and self.has_morphology
            and self.has_sandhi
            and self.has_samasa
            and self.has_semantic
        )

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    # ---------------------------------------------------------
    # Immutable enrichment
    # ---------------------------------------------------------

    def with_lexical(
        self,
        result: LexicalResolutionResult,
    ) -> "ResolutionResult":
        return ResolutionResult(
            context=self.context,
            lexical=result,
            morphology=self.morphology,
            sandhi=self.sandhi,
            samasa=self.samasa,
            semantic=self.semantic,
            diagnostics=self.diagnostics,
            confidence=self.confidence,
            succeeded=self.succeeded,
        )

    def with_morphology(
        self,
        result: MorphologicalResolutionResult,
    ) -> "ResolutionResult":
        return ResolutionResult(
            context=self.context,
            lexical=self.lexical,
            morphology=result,
            sandhi=self.sandhi,
            samasa=self.samasa,
            semantic=self.semantic,
            diagnostics=self.diagnostics,
            confidence=self.confidence,
            succeeded=self.succeeded,
        )

    def with_sandhi(
        self,
        result: SandhiResolutionResult,
    ) -> "ResolutionResult":
        return ResolutionResult(
            context=self.context,
            lexical=self.lexical,
            morphology=self.morphology,
            sandhi=result,
            samasa=self.samasa,
            semantic=self.semantic,
            diagnostics=self.diagnostics,
            confidence=self.confidence,
            succeeded=self.succeeded,
        )

    def with_samasa(
        self,
        result: SamasaResolutionResult,
    ) -> "ResolutionResult":
        return ResolutionResult(
            context=self.context,
            lexical=self.lexical,
            morphology=self.morphology,
            sandhi=self.sandhi,
            samasa=result,
            semantic=self.semantic,
            diagnostics=self.diagnostics,
            confidence=self.confidence,
            succeeded=self.succeeded,
        )

    def with_semantic(
        self,
        result: SemanticResolutionResult,
    ) -> "ResolutionResult":
        return ResolutionResult(
            context=self.context,
            lexical=self.lexical,
            morphology=self.morphology,
            sandhi=self.sandhi,
            samasa=self.samasa,
            semantic=result,
            diagnostics=self.diagnostics,
            confidence=self.confidence,
            succeeded=self.succeeded,
        )

    def __str__(self) -> str:
        return self.display_text

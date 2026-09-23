from __future__ import annotations

"""
SanskritAI
==========

Reader Result

Defines the immutable high-level result returned by the
Reader Engine.

ReaderResult is the final aggregation object produced after the
complete linguistic resolution pipeline has executed.

Pipeline
--------

ReaderContext
      │
      ▼
Resolution Pipeline
      │
      ├── Lexical
      ├── Morphology
      ├── Sandhi
      ├── Samasa
      ├── Semantic
      │
      ▼
ReaderResult

Unlike ResolutionResult, which represents one individual
resolution stage, ReaderResult represents the complete
linguistic understanding of one reader request.

Future versions will additionally aggregate

    • Pragmatics

    • Commentarial reasoning

    • Cross references

    • Canonical citations

    • AI reasoning

    • Knowledge graph links

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.reader.reader_context import ReaderContext

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


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by the Reader Engine.
    """

    context: ReaderContext

    lexical: LexicalResolutionResult | None = None

    morphology: MorphologicalResolutionResult | None = None

    sandhi: SandhiResolutionResult | None = None

    samasa: SamasaResolutionResult | None = None

    semantic: SemanticResolutionResult | None = None

    pragmatics: Any | None = None

    commentary: Any | None = None

    cross_references: tuple[Any, ...] = field(
        default_factory=tuple,
    )

    canonical_sources: tuple[Any, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Result"

    @property
    def display_text(self) -> str:
        return str(self.context.subject)

    @property
    def display_description(self) -> str:
        return (
            "Complete linguistic interpretation produced "
            "by the Reader Engine."
        )

    # ---------------------------------------------------------
    # Resolution Summary
    # ---------------------------------------------------------

    @property
    def lexical_available(self) -> bool:
        return self.lexical is not None

    @property
    def morphology_available(self) -> bool:
        return self.morphology is not None

    @property
    def sandhi_available(self) -> bool:
        return self.sandhi is not None

    @property
    def samasa_available(self) -> bool:
        return self.samasa is not None

    @property
    def semantic_available(self) -> bool:
        return self.semantic is not None

    @property
    def pragmatics_available(self) -> bool:
        return self.pragmatics is not None

    @property
    def commentary_available(self) -> bool:
        return self.commentary is not None

    # ---------------------------------------------------------
    # Completion
    # ---------------------------------------------------------

    @property
    def completed_stage_count(self) -> int:

        return sum(
            (
                self.lexical_available,
                self.morphology_available,
                self.sandhi_available,
                self.samasa_available,
                self.semantic_available,
                self.pragmatics_available,
                self.commentary_available,
            )
        )

    @property
    def total_stage_count(self) -> int:
        """
        Future-proof stage count.

        Current:

            Lexical
            Morphology
            Sandhi
            Samasa
            Semantic
            Pragmatics
            Commentary
        """
        return 7

    @property
    def completion_ratio(self) -> float:

        return (
            self.completed_stage_count
            / self.total_stage_count
        )

    @property
    def is_complete(self) -> bool:
        """
        Complete with currently implemented stages.
        """

        return (
            self.lexical_available
            and self.morphology_available
            and self.sandhi_available
            and self.samasa_available
            and self.semantic_available
        )

    # ---------------------------------------------------------
    # Collections
    # ---------------------------------------------------------

    @property
    def has_cross_references(self) -> bool:
        return bool(self.cross_references)

    @property
    def cross_reference_count(self) -> int:
        return len(self.cross_references)

    @property
    def has_canonical_sources(self) -> bool:
        return bool(self.canonical_sources)

    @property
    def canonical_source_count(self) -> int:
        return len(self.canonical_sources)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

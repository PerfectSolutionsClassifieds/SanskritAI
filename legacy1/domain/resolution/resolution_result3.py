from __future__ import annotations

"""
SanskritAI
==========

Resolution Result

Canonical output produced by the Resolution Pipeline.

Each linguistic stage enriches the same ResolutionResult
instance. The object therefore becomes the unified semantic
representation of a Sanskrit unit (word, sentence, śloka,
etc.).

Pipeline

    Lexical
        ↓
    Morphology
        ↓
    Sandhi
        ↓
    Samasa
        ↓
    Semantic
        ↓
    Pragmatics (future)
        ↓
    Commentary (future)

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)

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


@dataclass(frozen=True, slots=True)
class ResolutionResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical pipeline output.

    Every linguistic kernel enriches this object.
    """

    context: ResolutionContext

    lexical: LexicalResolutionResult | None = None

    morphology: MorphologicalResolutionResult | None = None

    sandhi: SandhiResolutionResult | None = None

    samasa: SamasaResolutionResult | None = None

    semantic: SemanticResolutionResult | None = None

    pragmatics: Any | None = None

    commentary: Any | None = None

    diagnostics: tuple[
        ResolutionDiagnostic,
        ...
    ] = field(default_factory=tuple)

    confidence: float = 1.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.context.identifier

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Resolution Result"

    @property
    def display_text(self) -> str:
        return str(self.context.subject)

    @property
    def display_description(self) -> str:
        return (
            "Canonical linguistic resolution produced "
            "by the Resolution Pipeline."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def subject(self):
        return self.context.subject

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
    def has_semantics(self) -> bool:
        return self.semantic is not None

    @property
    def has_pragmatics(self) -> bool:
        return self.pragmatics is not None

    @property
    def has_commentary(self) -> bool:
        return self.commentary is not None

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def succeeded(self) -> bool:
        return (
            self.has_lexical
            or self.has_morphology
            or self.has_sandhi
            or self.has_samasa
            or self.has_semantics
        )

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text

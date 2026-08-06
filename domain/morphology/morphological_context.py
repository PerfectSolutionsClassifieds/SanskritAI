from __future__ import annotations

"""
SanskritAI
==========

Morphological Context

Provides the canonical execution context for the Morphology
Kernel.

Unlike MorphologicalFeatures, which represent the OUTPUT of
analysis, this context represents the INPUT supplied to the
morphological analyzer.

The context aggregates all upstream linguistic knowledge so
that morphology can operate without repeatedly querying
repositories.

Relationship
------------

ResolutionContext
        │
        ▼
LexicalResolutionResult
        │
        ▼
DhatuResolutionResult
        │
        ▼
MorphologicalContext
        │
        ▼
MorphologicalAnalyzer

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.lexical.word_form import WordForm

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.dhatu.dhatu_resolution_result import (
    DhatuResolutionResult,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.domain.dhatu.dhatu_repository import (
    DhatuRepository,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MorphologicalContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution context for morphological analysis.
    """

    resolution_context: ResolutionContext

    word_form: WordForm

    lexical_result: LexicalResolutionResult | None = None

    dhatu_result: DhatuResolutionResult | None = None

    canonical_repository: CanonicalKnowledgeRepository | None = None

    dhatu_repository: DhatuRepository | None = None

    notes: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Morphological Context"

    @property
    def display_text(
        self,
    ) -> str:

        return self.word_form.display_text

    @property
    def display_description(
        self,
    ) -> str:

        return self.notes

    # ---------------------------------------------------------
    # Availability
    # ---------------------------------------------------------

    @property
    def has_lexical_result(
        self,
    ) -> bool:

        return self.lexical_result is not None

    @property
    def has_dhatu_result(
        self,
    ) -> bool:

        return self.dhatu_result is not None

    @property
    def has_canonical_repository(
        self,
    ) -> bool:

        return self.canonical_repository is not None

    @property
    def has_dhatu_repository(
        self,
    ) -> bool:

        return self.dhatu_repository is not None

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def canonical_entry(
        self,
    ):
        if self.lexical_result is None:
            return None

        return self.lexical_result.entry

    @property
    def canonical_sense(
        self,
    ):
        if self.lexical_result is None:
            return None

        return self.lexical_result.sense

    @property
    def dhatu(
        self,
    ):
        if self.dhatu_result is None:
            return None

        return self.dhatu_result.dhatu

    @property
    def root(
        self,
    ) -> str | None:

        if self.dhatu is None:
            return None

        return self.dhatu.root

    @property
    def lemma(
        self,
    ) -> str:

        return self.word_form.lemma.text

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text

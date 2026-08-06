from __future__ import annotations

"""
SanskritAI
==========

Default Lexical Resolution Strategy

Purpose
-------
Default implementation of the LexicalResolutionStrategy.

Unlike the Phase-1 implementation, this strategy no longer
performs dictionary lookups directly.

Instead it delegates all lexical retrieval to the
LexicalRepository adapter, which itself delegates to the
CanonicalKnowledgeRepository.

Future evolution
----------------

Current

    ResolutionContext
            │
            ▼
DefaultLexicalResolutionStrategy
            │
            ▼
LexicalRepository
            │
            ▼
CanonicalKnowledgeRepository

Future

    ResolutionContext
            │
            ▼
DefaultLexicalResolutionStrategy
            │
            ▼
LexicalLookupEngine
            │
            ▼
CanonicalKnowledgeRepository

The Lookup Engine will eventually perform

    • Sandhi normalization

    • Samāsa decomposition

    • Dhātu lookup

    • Lemma normalization

    • Ranking

    • Semantic disambiguation

Version
-------
v2.0.0
"""

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.lexical.lexical_resolution_strategy import (
    LexicalResolutionStrategy,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


class DefaultLexicalResolutionStrategy(
    LexicalResolutionStrategy,
):
    """
    Default lexical resolution strategy.

    Performs direct canonical lookup.

    No linguistic normalization is performed here.

    Future versions will replace the repository lookup with a
    dedicated LexicalLookupEngine.
    """

    def __init__(
        self,
        repository: LexicalRepository,
    ) -> None:

        self._repository = repository

    # ---------------------------------------------------------
    # Repository
    # ---------------------------------------------------------

    @property
    def repository(
        self,
    ) -> LexicalRepository:

        return self._repository

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Performs canonical lexical lookup.

        Lookup order

            1. Surface word-form

            2. Canonical entry

            3. Preferred sense
        """

        word_form = str(
            context.subject,
        )

        entries = (
            self.repository.find_entries_by_word_form(
                word_form,
            )
        )

        if not entries:

            return LexicalResolutionResult(
                context=context,
                succeeded=False,
                confidence=0.0,
                matched_word_form=word_form,
                normalized_word_form=word_form,
            )

        entry = entries[0]

        senses = self.repository.find_senses(
            entry.headword,
        )

        preferred_sense = (
            senses[0]
            if senses
            else None
        )

        ambiguity = len(
            senses,
        ) > 1

        confidence = (
            1.0
            if preferred_sense is not None
            else 0.50
        )

        return LexicalResolutionResult(
            context=context,
            entry=entry,
            sense=preferred_sense,
            matched_word_form=word_form,
            normalized_word_form=word_form,
            ambiguity_detected=ambiguity,
            succeeded=True,
            confidence=confidence,
        )

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Default Lexical Resolution Strategy"

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Canonical lexical lookup using the "
            "Canonical Knowledge Repository."
        )

from __future__ import annotations

"""
SanskritAI
==========

Default Lexical Resolution Strategy

Default implementation of the LexicalResolutionStrategy.

This implementation performs direct lexical lookup using the
configured LexicalRepository.

It intentionally contains no morphology, Sandhi, Samāsa,
Dhātu, or semantic reasoning. Those capabilities belong to
future specialized strategies.

Version
-------
v1.0.0
"""

from SanskritAI.domain.lexical.lexical_entry_collection import (
    LexicalEntryCollection,
)
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
        Performs direct lexical lookup.
        """

        subject = str(context.subject)

        entries: LexicalEntryCollection = (
            self.repository.find_by_word_form(
                subject
            )
        )

        confidence = (
            1.0
            if len(entries) == 1
            else 0.75
            if len(entries) > 1
            else 0.0
        )

        return LexicalResolutionResult(
            context=context,
            entries=entries,
            normalized_word_form=subject,
            matched_word_form=subject,
            succeeded=len(entries) > 0,
            confidence=confidence,
            ambiguity_detected=len(entries) > 1,
        )

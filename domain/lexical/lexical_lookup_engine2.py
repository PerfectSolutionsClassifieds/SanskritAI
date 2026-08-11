from __future__ import annotations

"""
SanskritAI
==========

Lexical Lookup Engine

Coordinates canonical lexical lookup.

The Lookup Engine is responsible for:

    • canonical word-form lookup

    • canonical lemma lookup

    • candidate ranking

    • preferred sense selection

    • ambiguity detection

The engine deliberately contains NO resolution logic.
It simply converts repository results into a
LexicalResolutionResult.

Architecture
------------

ResolutionContext
        │
        ▼
LexicalLookupEngine
        │
        ▼
CanonicalKnowledgeRepository
        │
        ▼
KnowledgeIndex
        │
        ▼
CanonicalDictionaryEntry
CanonicalDictionarySense

Version
-------
v2.1.0
"""

from __future__ import annotations

from SanskritAI.domain.lexical.lookup_candidate import (
    LookupCandidate,
)

from SanskritAI.domain.lexical.lookup_ranking_policy import (
    LookupRankingPolicy,
)

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.knowledge.repositories.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


class LexicalLookupEngine:
    """
    Canonical lexical lookup engine.
    """

    def __init__(
        self,
        repository: CanonicalKnowledgeRepository,
        ranking_policy: LookupRankingPolicy | None = None,
    ) -> None:

        self._repository = repository

        self._ranking_policy = (
            ranking_policy
            if ranking_policy is not None
            else LookupRankingPolicy()
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def repository(
        self,
    ) -> CanonicalKnowledgeRepository:
        return self._repository

    @property
    def ranking_policy(
        self,
    ) -> LookupRankingPolicy:
        return self._ranking_policy

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Performs canonical lexical lookup.

        Current behaviour

            1. Word-form lookup

            2. Convert entries → candidates

            3. Rank candidates

            4. Return canonical result

        Future versions may additionally perform

            • lemma normalization

            • sandhi expansion

            • samāsa decomposition

            • morphology expansion

            • semantic ranking

            • AI-assisted disambiguation
        """

        word_form = str(context.subject)

        # -------------------------------------------------
        # Canonical lookup
        # -------------------------------------------------

        entries = tuple(
            self.repository.find_entries_by_word_form(
                word_form,
            )
        )

        # -------------------------------------------------
        # Candidate construction
        # -------------------------------------------------

        candidates = tuple(
            LookupCandidate(
                entry=entry,
                matched_word_form=word_form,
            )
            for entry in entries
        )

        # -------------------------------------------------
        # Candidate ranking
        # -------------------------------------------------

        ranked_candidates = (
            self.ranking_policy.rank(
                candidates,
            )
        )

        preferred_candidate = (
            ranked_candidates[0]
            if ranked_candidates
            else None
        )

        preferred_entry: CanonicalDictionaryEntry | None = (
            preferred_candidate.entry
            if preferred_candidate
            else None
        )

        preferred_sense: CanonicalDictionarySense | None = (
            preferred_candidate.sense
            if preferred_candidate
            else None
        )

        # -------------------------------------------------
        # Resolution Result
        # -------------------------------------------------

        return LexicalResolutionResult(
            context=context,
            canonical_entry=preferred_entry,
            canonical_sense=preferred_sense,
            candidates=ranked_candidates,
            matched_word_form=word_form,
            normalized_word_form=word_form,
            ambiguity_detected=(
                len(ranked_candidates) > 1
            ),
            succeeded=(
                preferred_entry is not None
            ),
            confidence=(
                preferred_candidate.score
                if preferred_candidate
                else 0.0
            ),
        )

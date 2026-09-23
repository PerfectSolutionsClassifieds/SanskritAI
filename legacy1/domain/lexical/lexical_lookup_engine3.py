from __future__ import annotations

"""
SanskritAI
==========

Lexical Lookup Engine

Coordinates canonical lexical lookup.

Responsibilities
----------------

• canonical word-form lookup

• canonical lemma lookup

• candidate construction

• candidate ranking

• ambiguity detection

The engine deliberately contains NO lexical reasoning.

It simply transforms repository output into a
LexicalResolutionResult.

Version
-------
v2.2.0
"""

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

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
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

        Current pipeline

            ResolutionContext
                    ↓
            Canonical Repository
                    ↓
            LookupCandidate(s)
                    ↓
            Ranking Policy
                    ↓
            LexicalResolutionResult

        Future versions may additionally perform

            • lemma normalization

            • morphology expansion

            • sandhi decomposition

            • samāsa decomposition

            • semantic ranking

            • AI-assisted disambiguation
        """

        word_form = str(context.subject)

        # -------------------------------------------------
        # Repository lookup
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
        # Ranking
        # -------------------------------------------------

        ranked_candidates = self.ranking_policy.rank(
            candidates,
        )

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        confidence = (
            ranked_candidates[0].score
            if ranked_candidates
            else 0.0
        )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        return LexicalResolutionResult(
            context=context,
            candidates=ranked_candidates,
            matched_word_form=word_form,
            normalized_word_form=word_form,
            ambiguity_detected=(
                len(ranked_candidates) > 1
            ),
            succeeded=bool(ranked_candidates),
            confidence=confidence,
        )

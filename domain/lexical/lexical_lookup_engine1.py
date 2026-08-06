from __future__ import annotations

"""
SanskritAI
==========

Lexical Lookup Engine

The LexicalLookupEngine centralizes all lexical retrieval logic.

It is the ONLY component responsible for querying the canonical
knowledge repository for lexical information.

Resolution strategies should never access repositories directly.

Pipeline
--------

ResolutionContext
        │
        ▼
LexicalLookupEngine
        │
        ▼
CanonicalKnowledgeRepository
        │
        ▼
CanonicalDictionaryEntry
        │
        ▼
LookupRankingPolicy
        │
        ▼
LookupCandidate(s)

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.lexical.lookup_candidate import LookupCandidate
from SanskritAI.domain.lexical.lookup_ranking_policy import (
    LookupRankingPolicy,
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


@dataclass(slots=True)
class LexicalLookupEngine:
    """
    Central lexical lookup engine.

    Responsibilities
    ----------------
    • Query canonical repository
    • Convert repository objects into LookupCandidate objects
    • Apply ranking policy
    • Return ranked candidates
    """

    repository: CanonicalKnowledgeRepository

    ranking_policy: LookupRankingPolicy

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def lookup(
        self,
        context: ResolutionContext,
    ) -> tuple[LookupCandidate, ...]:
        """
        Performs lexical lookup.

        Parameters
        ----------
        context:
            Resolution context.

        Returns
        -------
        tuple[LookupCandidate, ...]
        """

        word_form = str(context.subject).strip()

        if not word_form:
            return ()

        #
        # Canonical repository lookup
        #
        entries = self.repository.find_entries_by_word_form(
            word_form,
        )

        candidates: list[LookupCandidate] = []

        for entry in entries:

            for sense in entry.senses:

                candidate = self._build_candidate(
                    entry=entry,
                    sense=sense,
                    matched_word_form=word_form,
                )

                candidates.append(candidate)

        #
        # Ranking
        #
        ranked = self.ranking_policy.rank(
            tuple(candidates),
        )

        return ranked

    # ---------------------------------------------------------
    # Candidate construction
    # ---------------------------------------------------------

    def _build_candidate(
        self,
        *,
        entry: CanonicalDictionaryEntry,
        sense: CanonicalDictionarySense,
        matched_word_form: str,
    ) -> LookupCandidate:

        return LookupCandidate(
            entry=entry,
            sense=sense,
            matched_word_form=matched_word_form,
            normalized_word_form=matched_word_form,
            score=self._initial_score(
                entry,
                sense,
            ),
        )

    # ---------------------------------------------------------
    # Initial scoring
    # ---------------------------------------------------------

    def _initial_score(
        self,
        entry: CanonicalDictionaryEntry,
        sense: CanonicalDictionarySense,
    ) -> float:
        """
        Baseline scoring before ranking policy.

        Future enhancements may include:

            • exact lemma match
            • headword frequency
            • dictionary priority
            • corpus frequency
            • semantic confidence
            • morphology confidence
            • context weighting
        """

        score = 1.0

        if sense.context is not None:
            score += 0.10

        if sense.source is not None:
            score += 0.05

        return score

from __future__ import annotations

"""
SanskritAI
==========

Lookup Ranking Policy

Defines the ranking policy used by the Lexical Lookup Engine.

The ranking policy is responsible only for ordering lexical
lookup candidates.

It intentionally knows nothing about repositories,
resolution strategies, or storage.

Relationship
------------

LexicalLookupEngine
        │
        ▼
LookupRankingPolicy
        │
        ▼
LookupCandidate*

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from typing import Iterable

from SanskritAI.domain.lexical.lookup_candidate import (
    LookupCandidate,
)


class LookupRankingPolicy(
    ABC,
):
    """
    Abstract ranking policy.

    A ranking policy receives an unordered collection of
    LookupCandidate objects and returns them ordered from
    best to worst.
    """

    @abstractmethod
    def rank(
        self,
        candidates: Iterable[LookupCandidate],
    ) -> tuple[
        LookupCandidate,
        ...
    ]:
        """
        Rank lookup candidates.

        Parameters
        ----------
        candidates:
            Unordered lookup candidates.

        Returns
        -------
        tuple[LookupCandidate, ...]
            Ranked candidates (highest score first).
        """
        raise NotImplementedError


class DefaultLookupRankingPolicy(
    LookupRankingPolicy,
):
    """
    Default ranking implementation.

    Current behaviour
    -----------------
    1. Higher score first.
    2. Alphabetical headword as deterministic tie-breaker.

    Future versions may incorporate:

        • lexical frequency

        • dictionary priority

        • semantic relevance

        • grammatical compatibility

        • contextual weighting

        • AI confidence
    """

    def rank(
        self,
        candidates: Iterable[LookupCandidate],
    ) -> tuple[
        LookupCandidate,
        ...
    ]:

        return tuple(
            sorted(
                candidates,
                key=lambda candidate: (
                    -candidate.score,
                    candidate.headword,
                ),
            )
        )

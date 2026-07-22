from __future__ import annotations

"""
SanskritAI
==========

Corpus Registry

In-memory registry for canonical Corpus objects.

The registry provides a lightweight repository abstraction used by
builders, parsers, acquisition providers, and future AI pipelines.

Version
-------
v0.1.0
"""

from typing import Iterator

from SanskritAI.common.identifiers.corpus_id import (
    CorpusId,
)

from SanskritAI.corpus.models.corpus import (
    Corpus,
)


class CorpusRegistry:
    """
    Registry of canonical Corpus objects.
    """

    def __init__(self) -> None:

        self._corpora: dict[
            CorpusId,
            Corpus,
        ] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        corpus: Corpus,
    ) -> None:
        """
        Register a Corpus.
        """

        self._corpora[
            corpus.id
        ] = corpus

    # ---------------------------------------------------------

    def unregister(
        self,
        corpus_id: CorpusId,
    ) -> None:
        """
        Remove a Corpus.
        """

        self._corpora.pop(
            corpus_id,
            None,
        )

    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered corpora.
        """

        self._corpora.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        corpus_id: CorpusId,
    ) -> Corpus | None:
        """
        Retrieve a Corpus.
        """

        return self._corpora.get(
            corpus_id
        )

    # ---------------------------------------------------------

    def exists(
        self,
        corpus_id: CorpusId,
    ) -> bool:
        """
        Returns True if the Corpus exists.
        """

        return corpus_id in self._corpora

    # ---------------------------------------------------------

    def all(self) -> list[Corpus]:
        """
        Return all registered corpora.
        """

        return list(
            self._corpora.values()
        )

    # ---------------------------------------------------------
    # Collection API
    # ---------------------------------------------------------

    def __contains__(
        self,
        corpus_id: CorpusId,
    ) -> bool:

        return corpus_id in self._corpora

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[Corpus]:

        return iter(
            self._corpora.values()
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._corpora
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"CorpusRegistry("

            f"count={len(self)})"

        )

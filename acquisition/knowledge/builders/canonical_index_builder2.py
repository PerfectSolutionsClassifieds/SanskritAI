from __future__ import annotations

"""
SanskritAI
==========

Canonical Index Builder

Purpose
-------
Builds and synchronizes every lookup index from the
immutable Canonical Sanskrit Knowledge Repository.

The builder performs a deterministic traversal of the
canonical lexical object graph.

Object Graph
------------

CanonicalLexicon
        │
        ▼
CanonicalDictionaryEntry
        │
        ▼
CanonicalDictionarySense
        │
        ├────────────► CanonicalContext
        │
        └────────────► CanonicalSource

Indexes Built
-------------

• HeadwordIndex

• LemmaIndex

• ContextIndex

• SourceIndex

Design Principles
-----------------

• Stateless

• Deterministic

• Rebuilds indexes from canonical data

• Owns no lexical data

• Safe to execute repeatedly

Version
-------
2.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)

from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)

from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)

from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


@dataclass(slots=True)
class CanonicalIndexBuilder:
    """
    Synchronizes every lookup index from the immutable
    canonical lexical graph.
    """

    headword_index: HeadwordIndex

    lemma_index: LemmaIndex

    context_index: ContextIndex

    source_index: SourceIndex

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...
        ],
    ) -> None:
        """
        Completely rebuild every index.
        """

        self.clear()

        for lexicon in lexicons:

            self._index_lexicon(
                lexicon,
            )

    # ---------------------------------------------------------
    # Lexicon
    # ---------------------------------------------------------

    def _index_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:

        for entry in lexicon:

            self._index_entry(
                entry,
            )

    # ---------------------------------------------------------
    # Entry
    # ---------------------------------------------------------

    def _index_entry(
        self,
        entry: CanonicalDictionaryEntry,
    ) -> None:

        #
        # Headword
        #

        self.headword_index.add(
            entry,
        )

        #
        # Lemma
        #

        if entry.lemma:

            self.lemma_index.add(
                entry,
            )

        #
        # Dictionary Senses
        #

        for sense in entry:

            self._index_sense(
                sense,
            )

    # ---------------------------------------------------------
    # Sense
    # ---------------------------------------------------------

    def _index_sense(
        self,
        sense: CanonicalDictionarySense,
    ) -> None:

        #
        # Context
        #

        if sense.context is not None:

            self.context_index.add(
                sense.context,
                sense,
            )

        #
        # Source
        #

        if sense.source is not None:

            self.source_index.add(
                sense.source,
                sense,
            )

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Clears every index.
        """

        self.headword_index.clear()

        self.lemma_index.clear()

        self.context_index.clear()

        self.source_index.clear()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "headwords": len(
                self.headword_index,
            ),

            "lemmas": len(
                self.lemma_index,
            ),

            "contexts": len(
                self.context_index,
            ),

            "sources": len(
                self.source_index,
            ),

        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalIndexBuilder("

            f"{self.summary()}"

            ")"

        )

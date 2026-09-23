from __future__ import annotations

"""
SanskritAI
==========

Canonical Index Builder

Purpose
-------
Builds every immutable lookup index from the canonical
lexical object graph.

The builder traverses

    CanonicalLexicon
        ↓
    CanonicalDictionaryEntry
        ↓
    CanonicalDictionarySense
        ↓
    CanonicalContext
        ↓
    CanonicalSource

and synchronizes

    • HeadwordIndex

    • LemmaIndex

    • ContextIndex

    • SourceIndex

The builder never owns lexical data.
It merely projects the canonical graph into optimized
lookup indexes.

Architecture
------------

CanonicalLexicon
        │
        ▼
CanonicalIndexBuilder
        │
        ├────────► HeadwordIndex
        ├────────► LemmaIndex
        ├────────► ContextIndex
        └────────► SourceIndex

Version
-------
1.0.0
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
            ...,
        ],
    ) -> None:
        """
        Rebuilds every index.

        Existing indexes are cleared before rebuilding.
        """

        self.clear()

        for lexicon in lexicons:

            self._index_lexicon(
                lexicon,
            )

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _index_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Indexes one canonical lexicon.
        """

        for entry in lexicon:

            #
            # Headword Index
            #

            self.headword_index.add(
                entry,
            )

            #
            # Lemma Index
            #

            if entry.lemma is not None:

                self.lemma_index.add(
                    entry,
                )

            #
            # Dictionary Senses
            #

            for sense in entry:

                #
                # Context Index
                #

                if sense.context is not None:

                    self.context_index.add(
                        sense.context,
                    )

                #
                # Source Index
                #

                if sense.source is not None:

                    self.source_index.add(
                        sense.source,
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

            "headwords":

                len(
                    self.headword_index,
                ),

            "lemmas":

                len(
                    self.lemma_index,
                ),

            "contexts":

                len(
                    self.context_index,
                ),

            "sources":

                len(
                    self.source_index,
                ),

        }

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalIndexBuilder("

            f"{self.summary()})"

        )

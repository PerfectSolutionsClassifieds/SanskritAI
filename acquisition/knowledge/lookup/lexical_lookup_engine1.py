from __future__ import annotations

"""
SanskritAI
==========

Lexical Lookup Engine

Purpose
-------
Provides the canonical query interface over the
Canonical Knowledge Repository.

Unlike registries, which own objects, and indexes,
which provide efficient retrieval, the Lookup Engine
coordinates multiple indexes to answer reader-oriented
queries.

Architecture
------------

                CanonicalKnowledgeRepository
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 HeadwordIndex        LemmaIndex        ContextIndex
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                     SourceIndex
                           │
                           ▼
                 LexicalLookupEngine
                           │
                           ▼
                     Reader UI
                           │
                           ▼
                 AI / Grammar / RAG

Responsibilities
----------------

• Lookup by headword

• Lookup by lemma

• Lookup by context

• Lookup by source

• Unified lexical search

• Future fuzzy search

• Future semantic search

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


@dataclass(slots=True)
class LexicalLookupEngine:
    """
    Unified lexical lookup engine.
    """

    headword_index: HeadwordIndex

    lemma_index: LemmaIndex

    context_index: ContextIndex

    source_index: SourceIndex

    # ---------------------------------------------------------
    # Headword Lookup
    # ---------------------------------------------------------

    def lookup_headword(
        self,
        headword: str,
    ):
        """
        Lookup by canonical headword.
        """

        return self.headword_index.lookup(
            headword,
        )

    def prefix_search(
        self,
        prefix: str,
    ):
        """
        Prefix lookup.
        """

        return self.headword_index.prefix_search(
            prefix,
        )

    # ---------------------------------------------------------
    # Lemma Lookup
    # ---------------------------------------------------------

    def lookup_lemma(
        self,
        lemma_id: str,
    ):
        """
        Lookup by lemma identifier.
        """

        return self.lemma_index.lookup(
            lemma_id,
        )

    def lookup_lemma_text(
        self,
        lemma_text: str,
    ):
        """
        Lookup by normalized lemma.
        """

        return self.lemma_index.lookup_text(
            lemma_text,
        )

    # ---------------------------------------------------------
    # Context Lookup
    # ---------------------------------------------------------

    def lookup_context(
        self,
        context_id: str,
    ):
        """
        Lookup one context.
        """

        return self.context_index.lookup(
            context_id,
        )

    def contexts_for_purana(
        self,
        purana_name: str,
    ):
        """
        Returns every context belonging to one Purāṇa.
        """

        return self.context_index.by_purana(
            purana_name,
        )

    def contexts_for_chapter(
        self,
        chapter_identifier: str,
    ):
        """
        Returns every context in one chapter.
        """

        return self.context_index.by_chapter(
            chapter_identifier,
        )

    def contexts_for_sloka(
        self,
        sloka_identifier: str,
    ):
        """
        Returns every context in one śloka.
        """

        return self.context_index.by_sloka(
            sloka_identifier,
        )

    # ---------------------------------------------------------
    # Source Lookup
    # ---------------------------------------------------------

    def lookup_source(
        self,
        source_id: str,
    ):
        """
        Lookup by source id.
        """

        return self.source_index.lookup(
            source_id,
        )

    def lookup_source_name(
        self,
        source_name: str,
    ):
        """
        Lookup by canonical source name.
        """

        return self.source_index.lookup_name(
            source_name,
        )

    def lookup_source_short_name(
        self,
        short_name: str,
    ):
        """
        Lookup by abbreviated source name.
        """

        return self.source_index.lookup_short_name(
            short_name,
        )

    # ---------------------------------------------------------
    # Unified Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> dict:
        """
        Unified lexical lookup.

        Future versions will extend this with

            • fuzzy lookup

            • semantic search

            • grammatical normalization

            • contextual ranking
        """

        return {

            "headword": self.lookup_headword(
                query,
            ),

            "lemma": self.lookup_lemma_text(
                query,
            ),

            "prefix_matches": self.prefix_search(
                query,
            ),

        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "headwords":
                len(self.headword_index),

            "lemmas":
                len(self.lemma_index),

            "contexts":
                len(self.context_index),

            "sources":
                len(self.source_index),

        }

    def __str__(
        self,
    ) -> str:

        return (
            "LexicalLookupEngine("
            "Headword + Lemma + Context + Source)"
        )

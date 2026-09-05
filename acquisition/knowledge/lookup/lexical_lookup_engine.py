from __future__ import annotations

"""
SanskritAI
==========

Lexical Lookup Engine

Purpose
-------
Provides the canonical query interface over the Canonical Knowledge Repository.

Unlike registries, which own objects, and indexes, which provide efficient retrieval,
the Lookup Engine coordinates multiple indexes to answer reader-oriented queries.

Architecture
------------

CanonicalKnowledgeRepository
│
├── HeadwordIndex
├── LemmaIndex
├── ContextIndex
└── SourceIndex
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
• Lookup by source name
• Lookup by source short name
• Unified lexical search

Source Lookup Semantics
-----------------------

The SourceIndex is a many-to-one index:

source_id
│
├── sense 1
├── sense 2
└── sense 3

The lookup engine exposes:

lookup_source(source_id) → all matching senses as a tuple
lookup_source_name(source_name) → all matching senses
lookup_source_short_name(short_name) → all matching senses

Version
-------
1.1.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)
from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)
from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
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
        """Lookup by canonical headword."""
        return self.headword_index.lookup(
            headword,
        )

    def prefix_search(
        self,
        prefix: str,
    ):
        """Prefix lookup."""
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
        """Lookup by canonical lemma identifier."""
        return self.lemma_index.lookup(
            lemma_id,
        )

    def lookup_lemma_text(
        self,
        lemma_text: str,
    ):
        """Lookup by normalized lemma text."""
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
        """Lookup all lexical senses associated with one context."""
        return self.context_index.lookup(
            context_id,
        )

    def contexts_for_purana(
        self,
        purana_name: str,
    ):
        """Return every lexical sense belonging to one Purāṇa."""
        return self.context_index.by_purana(
            purana_name,
        )

    def contexts_for_chapter(
        self,
        chapter_identifier: str,
    ):
        """Return every lexical sense belonging to one chapter."""
        return self.context_index.by_chapter(
            chapter_identifier,
        )

    def contexts_for_sloka(
        self,
        sloka_identifier: str,
    ):
        """Return every lexical sense belonging to one śloka."""
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
        """Lookup all lexical senses associated with a source ID.

        Returns
        -------
        tuple[CanonicalDictionarySense, ...]
        """
        return self.source_index.lookup(
            source_id,
        )

    def lookup_source_name(
        self,
        source_name: str,
    ):
        """Lookup every lexical sense associated with a canonical source name."""
        return self.source_index.lookup_name(
            source_name,
        )

    def lookup_source_short_name(
        self,
        short_name: str,
    ):
        """Lookup every lexical sense associated with a source abbreviation."""
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
        """Unified lexical lookup."""
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
            "headwords": len(self.headword_index),
            "lemmas": len(self.lemma_index),
            "contexts": len(self.context_index),
            "sources": len(self.source_index),
        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return (
            "LexicalLookupEngine("
            "Headword + Lemma + Context + Source)"
        )

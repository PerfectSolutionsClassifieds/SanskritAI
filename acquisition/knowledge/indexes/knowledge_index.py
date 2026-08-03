from __future__ import annotations

"""
SanskritAI
==========

Knowledge Index

Purpose
-------
Aggregates every lookup index used by the
Canonical Sanskrit Knowledge Repository.

The KnowledgeIndex provides a single façade over all
lexical indexes and owns the LexicalLookupEngine.

Architecture
------------

KnowledgeIndex

    ├── HeadwordIndex

    ├── LemmaIndex

    ├── ContextIndex

    ├── SourceIndex

    └── LexicalLookupEngine

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

from SanskritAI.acquisition.knowledge.lookup.lexical_lookup_engine import (
    LexicalLookupEngine,
)


@dataclass(slots=True)
class KnowledgeIndex:
    """
    Aggregates all lexical indexes into one query layer.
    """

    headword_index: HeadwordIndex

    lemma_index: LemmaIndex

    context_index: ContextIndex

    source_index: SourceIndex

    lookup_engine: LexicalLookupEngine

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

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

            "headwords": len(self.headword_index),

            "lemmas": len(self.lemma_index),

            "contexts": len(self.context_index),

            "sources": len(self.source_index),

        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (

            "KnowledgeIndex("

            f"{self.summary()}"

            ")"

        )

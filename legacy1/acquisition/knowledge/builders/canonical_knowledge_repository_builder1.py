from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository Builder

Purpose
-------
Constructs a fully initialized immutable
CanonicalKnowledgeRepository.

The builder assembles all registries, indexes and the
LexicalLookupEngine into one coherent repository.

Architecture
------------

Acquisition Pipelines
        │
        ▼
Canonical Objects
        │
        ▼
CanonicalKnowledgeRepositoryBuilder
        │
        ├───────────────┐
        ▼               ▼
 Registries         Indexes
        │               │
        └───────┬───────┘
                ▼
      LexicalLookupEngine
                │
                ▼
CanonicalKnowledgeRepository

Responsibilities
----------------

• Build registries

• Populate registries

• Build indexes

• Populate indexes

• Construct Lookup Engine

• Produce immutable Repository

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.acquisition.knowledge.lookup.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.acquisition.knowledge.registries.lexical_registry import (
    LexicalRegistry,
)

from SanskritAI.acquisition.knowledge.registries.lemma_registry import (
    LemmaRegistry,
)

from SanskritAI.acquisition.knowledge.registries.source_registry import (
    SourceRegistry,
)

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
class CanonicalKnowledgeRepositoryBuilder:
    """
    Builder responsible for assembling the complete
    Canonical Knowledge Repository.
    """

    lexical_registry: LexicalRegistry = field(
        default_factory=LexicalRegistry,
    )

    lemma_registry: LemmaRegistry = field(
        default_factory=LemmaRegistry,
    )

    source_registry: SourceRegistry = field(
        default_factory=SourceRegistry,
    )

    headword_index: HeadwordIndex = field(
        default_factory=HeadwordIndex,
    )

    lemma_index: LemmaIndex = field(
        default_factory=LemmaIndex,
    )

    context_index: ContextIndex = field(
        default_factory=ContextIndex,
    )

    source_index: SourceIndex = field(
        default_factory=SourceIndex,
    )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register_lexicon(
        self,
        lexicon,
    ) -> None:

        self.lexical_registry.register(
            lexicon,
        )

    def register_lemma(
        self,
        lemma,
    ) -> None:

        self.lemma_registry.register(
            lemma,
        )

    def register_source(
        self,
        source,
    ) -> None:

        self.source_registry.register(
            source,
        )

    # ---------------------------------------------------------
    # Index Construction
    # ---------------------------------------------------------

    def build_indexes(
        self,
    ) -> None:
        """
        Builds every index from the registries.

        Future versions will populate indexes from the
        canonical lexical repository.
        """

        # Placeholder for future synchronization logic.

        # Example:

        # self.headword_index.build(...)
        # self.lemma_index.build(...)
        # self.context_index.build(...)
        # self.source_index.build(...)

        return

    # ---------------------------------------------------------
    # Lookup Engine
    # ---------------------------------------------------------

    def build_lookup_engine(
        self,
    ) -> LexicalLookupEngine:

        return LexicalLookupEngine(

            headword_index=self.headword_index,

            lemma_index=self.lemma_index,

            context_index=self.context_index,

            source_index=self.source_index,

        )

    # ---------------------------------------------------------
    # Repository
    # ---------------------------------------------------------

    def build(
        self,
    ) -> CanonicalKnowledgeRepository:
        """
        Builds a fully initialized repository.
        """

        self.build_indexes()

        lookup_engine = self.build_lookup_engine()

        return CanonicalKnowledgeRepository(

            lexical_registry=self.lexical_registry,

            lemma_registry=self.lemma_registry,

            source_registry=self.source_registry,

            headword_index=self.headword_index,

            lemma_index=self.lemma_index,

            context_index=self.context_index,

            source_index=self.source_index,

            lookup_engine=lookup_engine,

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "registries": {

                "lexicons": len(self.lexical_registry),

                "lemmas": len(self.lemma_registry),

                "sources": len(self.source_registry),

            },

            "indexes": {

                "headwords": len(self.headword_index),

                "lemmas": len(self.lemma_index),

                "contexts": len(self.context_index),

                "sources": len(self.source_index),

            },

        }

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalKnowledgeRepositoryBuilder()"
        )

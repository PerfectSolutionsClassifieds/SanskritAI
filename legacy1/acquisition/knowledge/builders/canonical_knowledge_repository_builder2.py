from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository Builder

Purpose
-------
Constructs and synchronizes a complete
CanonicalKnowledgeRepository.

The builder owns the complete construction lifecycle of the
repository while delegating index synchronization to the
CanonicalIndexBuilder.

Responsibilities
----------------

• Register Canonical Lexicons

• Build Registries

• Synchronize Lookup Indexes

• Construct Lookup Engine

Architecture
------------

                    CanonicalLexicons
                           │
                           ▼
        CanonicalKnowledgeRepositoryBuilder
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
     LexicalRegistry  LemmaRegistry  SourceRegistry
            │
            ▼
     CanonicalIndexBuilder
            │
            ├────────► HeadwordIndex
            ├────────► LemmaIndex
            ├────────► ContextIndex
            └────────► SourceIndex
            │
            ▼
     LexicalLookupEngine
            │
            ▼
CanonicalKnowledgeRepository

Version
-------
2.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)


@dataclass(slots=True)
class CanonicalKnowledgeRepositoryBuilder:
    """
    Builder responsible for constructing a fully
    synchronized CanonicalKnowledgeRepository.
    """

    repository: CanonicalKnowledgeRepository

    index_builder: CanonicalIndexBuilder

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...
        ],
    ) -> CanonicalKnowledgeRepository:
        """
        Build an entire repository from canonical lexicons.
        """

        self.clear()

        self._register_lexicons(
            lexicons,
        )

        self._synchronize_indexes()

        return self.repository

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def _register_lexicons(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...
        ],
    ) -> None:

        for lexicon in lexicons:

            self.repository.lexical_registry.register(
                lexicon,
            )

    # ---------------------------------------------------------
    # Synchronization
    # ---------------------------------------------------------

    def _synchronize_indexes(
        self,
    ) -> None:
        """
        Delegates index construction to the dedicated
        CanonicalIndexBuilder.
        """

        self.index_builder.build(

            self.repository.lexical_registry.all()

        )

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Clears repository state prior to rebuilding.
        """

        #
        # Registries
        #

        self.repository.lexical_registry.clear()

        self.repository.lemma_registry.clear()

        self.repository.source_registry.clear()

        #
        # Indexes
        #

        self.index_builder.clear()

    # ---------------------------------------------------------
    # Incremental Update
    # ---------------------------------------------------------

    def add_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Incrementally registers one lexicon and rebuilds
        indexes.
        """

        self.repository.lexical_registry.register(
            lexicon,
        )

        self._synchronize_indexes()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "repository":

                self.repository.summary(),

            "indexes":

                self.index_builder.summary(),

        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalKnowledgeRepositoryBuilder("

            f"{self.summary()}"

            ")"

        )

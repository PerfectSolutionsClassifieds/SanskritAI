from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository Builder

Purpose
-------
Constructs and synchronizes the Canonical Sanskrit
Knowledge Repository.

Responsibilities

    • Populate Registries

    • Synchronize KnowledgeIndex

Version
-------
3.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)


@dataclass(slots=True)
class CanonicalKnowledgeRepositoryBuilder:
    """
    Repository construction orchestrator.
    """

    repository: CanonicalKnowledgeRepository

    index_builder: CanonicalIndexBuilder

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def build(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> CanonicalKnowledgeRepository:

        self.clear()

        self._populate_registries(
            lexicons,
        )

        self._synchronize_indexes()

        return self.repository

    # ---------------------------------------------------------
    # Registries
    # ---------------------------------------------------------

    def _populate_registries(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> None:

        for lexicon in lexicons:

            self.repository.lexical_registry.register(
                lexicon,
            )

    # ---------------------------------------------------------
    # Indexes
    # ---------------------------------------------------------

    def _synchronize_indexes(
        self,
    ) -> None:

        self.index_builder.build(

            self.repository.lexical_registry.all()

        )

    # ---------------------------------------------------------
    # Incremental
    # ---------------------------------------------------------

    def add_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:

        self.repository.lexical_registry.register(
            lexicon,
        )

        self._synchronize_indexes()

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        #
        # Registries
        #

        self.repository.lexical_registry.clear()

        self.repository.lemma_registry.clear()

        self.repository.source_registry.clear()

        #
        # Knowledge Index
        #

        self.repository.knowledge_index.clear()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "repository":

                self.repository.summary(),

        }

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalKnowledgeRepositoryBuilder("

            f"{self.summary()}"

            ")"

        )

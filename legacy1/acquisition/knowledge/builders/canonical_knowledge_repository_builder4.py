
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
----------------

    • Populate the canonical lexical repository
    • Synchronize the CanonicalIndexBuilder
    • Maintain deterministic rebuild semantics
    • Support incremental lexicon addition

Architectural Role
------------------

CanonicalLexicon
        │
        ▼
CanonicalKnowledgeRepositoryBuilder
        │
        ├──────────► CanonicalKnowledgeRepository
        │
        └──────────► CanonicalIndexBuilder

The builder is an orchestration component.

It does not own canonical lexical data.

Version
-------
4.0.0
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
    Orchestrates construction of the canonical knowledge repository.

    The builder owns no lexical state.  All canonical data remains
    owned by the supplied repository and its underlying repositories.

    Index construction is delegated to CanonicalIndexBuilder.
    """

    repository: CanonicalKnowledgeRepository

    index_builder: CanonicalIndexBuilder

    # =========================================================
    # Public Build API
    # =========================================================

    def build(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> CanonicalKnowledgeRepository:
        """
        Rebuild the repository from the supplied lexicons.

        Build semantics are replacement semantics:

            previous state
                    ↓
                 clear
                    ↓
            register lexicons
                    ↓
            synchronize indexes
                    ↓
              return repository
        """

        self.clear()

        self._populate_lexical_repository(
            lexicons,
        )

        self._synchronize_indexes()

        return self.repository

    # =========================================================
    # Lexical Repository
    # =========================================================

    def _populate_lexical_repository(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> None:
        """
        Populate the canonical lexical repository.

        CanonicalKnowledgeRepository exposes the lexical repository
        as ``lexical_repository``.
        """

        lexical_repository = self.repository.lexical_repository

        for lexicon in lexicons:

            lexical_repository.register(
                lexicon,
            )

    # =========================================================
    # Index Synchronization
    # =========================================================

    def _synchronize_indexes(
        self,
    ) -> None:
        """
        Rebuild every lookup index from the registered lexicons.
        """

        lexicons = (
            self.repository.lexical_repository.all()
        )

        self.index_builder.build(
            lexicons,
        )

    # =========================================================
    # Incremental Addition
    # =========================================================

    def add_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Add one lexicon incrementally and rebuild the indexes.
        """

        self.repository.lexical_repository.register(
            lexicon,
        )

        self._synchronize_indexes()

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(
        self,
    ) -> None:
        """
        Clear canonical lexical repository state and lookup indexes.

        The builder does not directly manipulate individual legacy
        registries.  Repository ownership remains centralized in
        CanonicalKnowledgeRepository.
        """

        self.repository.lexical_repository.clear()

        self.index_builder.headword_index.clear()

        self.index_builder.lemma_index.clear()

        self.index_builder.context_index.clear()

        self.index_builder.source_index.clear()

    # =========================================================
    # Diagnostics
    # =========================================================

    def summary(
        self,
    ) -> dict:
        """
        Return a compact builder diagnostic summary.

        The repository remains the authoritative source for
        repository-level diagnostics.
        """

        repository_summary = {}

        summary_method = getattr(
            self.repository,
            "summary",
            None,
        )

        if callable(summary_method):
            repository_summary = summary_method()

        return {
            "repository": repository_summary,
        }

    # =========================================================
    # Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:
        return (
            "CanonicalKnowledgeRepositoryBuilder("
            f"{self.summary()}"
            ")"
        )

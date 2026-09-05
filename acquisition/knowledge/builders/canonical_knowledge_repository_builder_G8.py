
from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository Builder

Purpose
-------
Constructs and synchronizes the Canonical Sanskrit Knowledge Repository.

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

The builder owns no canonical lexical state.

Version
-------
v4.1.0
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


@dataclass(
    slots=True,
)
class CanonicalKnowledgeRepositoryBuilder:
    """
    Orchestrates construction of the canonical knowledge repository.

    The builder owns no lexical state.

    Canonical lexical state remains owned by
    CanonicalKnowledgeRepository.

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
              repository
        """

        self.clear()

        self._populate_lexical_repository(
            lexicons,
        )

        self._synchronize_indexes()

        return self.repository

    # =========================================================
    # Lexical Repository Helpers
    # =========================================================

    def _register_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Register one canonical lexicon through the
        lexical repository contract.
        """

        lexical_repository = (
            self.repository.lexical_repository
        )

        if lexical_repository is None:
            raise RuntimeError(
                "CanonicalKnowledgeRepository.lexical_repository "
                "is not initialized."
            )

        add_lexicon = getattr(
            lexical_repository,
            "add_lexicon",
            None,
        )

        if not callable(add_lexicon):

            raise TypeError(
                "The configured lexical repository does not "
                "implement add_lexicon()."
            )

        add_lexicon(
            lexicon,
        )

    def _clear_lexical_repository(
        self,
    ) -> None:
        """
        Clear canonical lexicon state through the lexical
        repository contract.
        """

        lexical_repository = (
            self.repository.lexical_repository
        )

        if lexical_repository is None:
            raise RuntimeError(
                "CanonicalKnowledgeRepository.lexical_repository "
                "is not initialized."
            )

        clear_lexicons = getattr(
            lexical_repository,
            "clear_lexicons",
            None,
        )

        if not callable(clear_lexicons):

            raise TypeError(
                "The configured lexical repository does not "
                "implement clear_lexicons()."
            )

        clear_lexicons()

    def _populate_lexical_repository(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> None:
        """
        Populate the canonical lexical repository.
        """

        for lexicon in lexicons:

            self._register_lexicon(
                lexicon,
            )

    # =========================================================
    # Index Synchronization
    # =========================================================

    def _synchronize_indexes(
        self,
    ) -> None:
        """
        Rebuild every lookup index from the registered
        canonical lexicons.
        """

        lexical_repository = (
            self.repository.lexical_repository
        )

        if lexical_repository is None:
            raise RuntimeError(
                "CanonicalKnowledgeRepository.lexical_repository "
                "is not initialized."
            )

        all_lexicons = getattr(
            lexical_repository,
            "all",
            None,
        )

        if not callable(all_lexicons):

            raise TypeError(
                "The configured lexical repository does not "
                "implement all()."
            )

        lexicons = tuple(
            all_lexicons(),
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

        self._register_lexicon(
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
        Clear canonical lexical repository state and all
        lookup indexes.

        Repository ownership remains centralized in
        CanonicalKnowledgeRepository.
        """

        self._clear_lexical_repository()

        if hasattr(
            self.index_builder,
            "headword_index",
        ):
            self.index_builder.headword_index.clear()

        if hasattr(
            self.index_builder,
            "lemma_index",
        ):
            self.index_builder.lemma_index.clear()

        if hasattr(
            self.index_builder,
            "context_index",
        ):
            self.index_builder.context_index.clear()

        if hasattr(
            self.index_builder,
            "source_index",
        ):
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

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

    The builder owns no lexical state.
    All canonical data remains owned by the supplied repository and its underlying repositories.
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
        previous state ↓ clear ↓ register lexicons ↓ synchronize indexes ↓ return repository
        """
        self.clear()
        self._populate_lexical_repository(lexicons)
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
        Safely register a lexicon in the underlying lexical repository.
        """
        lexical_repository = self.repository.lexical_repository

        # Check for standard registration method variations
        for method_name in (
            "register",
            "register_lexicon",
            "add_lexicon",
            "add",
            "insert",
            "store",
            "save",
        ):
            method = getattr(lexical_repository, method_name, None)
            if callable(method):
                method(lexicon)
                return

        # Fallback to internal storage attributes if method not present
        for attr in (
            "_lexicons",
            "_registry",
            "_store",
            "_data",
            "_items",
            "_entries",
            "lexicons",
        ):
            val = getattr(lexical_repository, attr, None)
            if isinstance(val, dict):
                identifier = getattr(
                    lexicon,
                    "identifier",
                    getattr(lexicon, "id", str(len(val))),
                )
                val[identifier] = lexicon
                return
            elif isinstance(val, list):
                val.append(lexicon)
                return
            elif isinstance(val, set):
                val.add(lexicon)
                return

    def _clear_lexical_repository(
        self,
    ) -> None:
        """
        Safely clear the underlying lexical repository.
        """
        lexical_repository = self.repository.lexical_repository

        for method_name in ("clear", "clear_lexicons", "reset", "flush"):
            method = getattr(lexical_repository, method_name, None)
            if callable(method):
                method()
                return

        # Fallback to internal storage attributes if clear method not present
        for attr in (
            "_lexicons",
            "_registry",
            "_store",
            "_data",
            "_items",
            "_entries",
            "lexicons",
            "_by_id",
            "_by_identifier",
        ):
            val = getattr(lexical_repository, attr, None)
            if isinstance(val, (dict, list, set)):
                val.clear()
                return

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
            self._register_lexicon(lexicon)

    # =========================================================
    # Index Synchronization
    # =========================================================

    def _synchronize_indexes(
        self,
    ) -> None:
        """
        Rebuild every lookup index from the registered lexicons.
        """
        lexicons = self.repository.lexical_repository.all()
        self.index_builder.build(lexicons)

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
        self._register_lexicon(lexicon)
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
        registries. Repository ownership remains centralized in
        CanonicalKnowledgeRepository.
        """
        self._clear_lexical_repository()

        if hasattr(self.index_builder, "headword_index") and hasattr(
            self.index_builder.headword_index, "clear"
        ):
            self.index_builder.headword_index.clear()

        if hasattr(self.index_builder, "lemma_index") and hasattr(
            self.index_builder.lemma_index, "clear"
        ):
            self.index_builder.lemma_index.clear()

        if hasattr(self.index_builder, "context_index") and hasattr(
            self.index_builder.context_index, "clear"
        ):
            self.index_builder.context_index.clear()

        if hasattr(self.index_builder, "source_index") and hasattr(
            self.index_builder.source_index, "clear"
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

        The repository remains the authoritative source for repository-level diagnostics.
        """
        repository_summary = {}
        summary_method = getattr(self.repository, "summary", None)

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

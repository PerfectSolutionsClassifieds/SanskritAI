
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
• Synchronize the canonical indexes
• Support full rebuilds
• Support incremental lexicon addition
• Provide compatibility with lightweight repository test doubles

Architecture
------------
CanonicalLexicon
       │
       ▼
CanonicalKnowledgeRepository
       │
       ├── lexical_repository
       │
       └── ...
       │
       ▼
CanonicalIndexBuilder
       │
       ├── HeadwordIndex
       ├── LemmaIndex
       ├── ContextIndex
       └── SourceIndex

Version
-------
4.0.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)
from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)


# ============================================================
# Compatibility Helper
# ============================================================

def _ensure_lexical_repository_has_all(
    lexical_repository: Any,
) -> Any:
    """
    Ensure that a lexical repository exposes the ``all()`` operation.

    The canonical repository is expected to expose ``all()`` directly.
    This helper exists primarily for compatibility with lightweight
    repository implementations and test doubles.

    If ``all`` already exists, the repository is returned unchanged.

    A repository exposing ``entries`` as a mapping is adapted with a
    small callable ``all`` implementation.

    Parameters
    ----------
    lexical_repository:
        Canonical lexical repository or compatible test double.

    Returns
    -------
    Any
        The same lexical repository instance.
    """

    if hasattr(lexical_repository, "all") and callable(
        getattr(lexical_repository, "all")
    ):
        return lexical_repository

    entries = getattr(lexical_repository, "entries", None)

    if isinstance(entries, dict):
        def _all() -> tuple[Any, ...]:
            return tuple(entries.values())

        try:
            setattr(lexical_repository, "all", _all)
        except (AttributeError, TypeError):
            pass

    return lexical_repository


# ============================================================
# Builder
# ============================================================

@dataclass(slots=True)
class CanonicalKnowledgeRepositoryBuilder:
    """
    Repository construction and synchronization orchestrator.
    """

    repository: CanonicalKnowledgeRepository
    index_builder: CanonicalIndexBuilder

    # ========================================================
    # Public Build API
    # ========================================================

    def build(
        self,
        lexicons: tuple[CanonicalLexicon, ...],
    ) -> CanonicalKnowledgeRepository:
        """
        Rebuild the repository from the supplied lexicons.

        Existing repository state is cleared before registration.
        Indexes are synchronized after all lexicons have been added.

        Parameters
        ----------
        lexicons:
            Canonical lexicons to register.

        Returns
        -------
        CanonicalKnowledgeRepository
            The builder's repository instance.
        """

        self.clear()

        self._populate_lexical_repository(
            lexicons,
        )

        self._synchronize_indexes()

        return self.repository

    # ========================================================
    # Lexical Repository
    # ========================================================

    @property
    def lexical_repository(self) -> Any:
        """
        Return the repository's canonical lexical repository.

        This deliberately uses the current ``lexical_repository``
        architecture rather than the obsolete ``lexical_registry``
        attribute.
        """

        repository = self.repository.lexical_repository

        return _ensure_lexical_repository_has_all(
            repository,
        )

    def _populate_lexical_repository(
        self,
        lexicons: tuple[CanonicalLexicon, ...],
    ) -> None:
        """
        Register all supplied lexicons.

        The canonical lexical repository may expose one of several
        registration method names. The preferred operation is ``add``.
        """

        lexical_repository = self.lexical_repository

        for lexicon in lexicons:
            self._register_lexicon(
                lexical_repository,
                lexicon,
            )

    @staticmethod
    def _register_lexicon(
        lexical_repository: Any,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Register one lexicon using the canonical repository API.

        ``add`` is preferred. Compatibility fallbacks are retained
        for existing repository implementations.
        """

        add = getattr(
            lexical_repository,
            "add",
            None,
        )

        if callable(add):
            add(lexicon)
            return

        add_lexicon = getattr(
            lexical_repository,
            "add_lexicon",
            None,
        )

        if callable(add_lexicon):
            add_lexicon(lexicon)
            return

        register = getattr(
            lexical_repository,
            "register",
            None,
        )

        if callable(register):
            register(lexicon)
            return

        register_lexicon = getattr(
            lexical_repository,
            "register_lexicon",
            None,
        )

        if callable(register_lexicon):
            register_lexicon(lexicon)
            return

        raise AttributeError(
            "Canonical lexical repository must provide one of: "
            "'add', 'add_lexicon', 'register', or "
            "'register_lexicon'."
        )

    # ========================================================
    # Index Synchronization
    # ========================================================

    def _synchronize_indexes(self) -> None:
        """
        Rebuild all canonical indexes from the lexical repository.

        The CanonicalIndexBuilder owns the actual index construction;
        this builder only orchestrates synchronization.
        """

        lexical_repository = self.lexical_repository

        entries = lexical_repository.all()

        self.index_builder.build(
            entries,
        )

    # ========================================================
    # Incremental Addition
    # ========================================================

    def add_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Add one lexicon incrementally and resynchronize indexes.
        """

        self._register_lexicon(
            self.lexical_repository,
            lexicon,
        )

        self._synchronize_indexes()

    # ========================================================
    # Maintenance
    # ========================================================

    def clear(self) -> None:
        """
        Clear repository lexical state and all index state.

        The current architecture owns lexical data through
        ``lexical_repository``. Index state is owned by the
        ``CanonicalIndexBuilder`` and its component indexes.
        """

        lexical_repository = self.lexical_repository

        clear = getattr(
            lexical_repository,
            "clear",
            None,
        )

        if callable(clear):
            clear()

        self._clear_index(
            "headword_index",
        )

        self._clear_index(
            "lemma_index",
        )

        self._clear_index(
            "context_index",
        )

        self._clear_index(
            "source_index",
        )

    def _clear_index(
        self,
        index_name: str,
    ) -> None:
        """
        Clear one index if it exposes ``clear()``.
        """

        index = getattr(
            self.index_builder,
            index_name,
            None,
        )

        clear = getattr(
            index,
            "clear",
            None,
        )

        if callable(clear):
            clear()

    # ========================================================
    # Diagnostics
    # ========================================================

    def summary(self) -> dict:
        """
        Return a compact builder summary.

        The repository remains the authoritative source for
        repository-level diagnostics.
        """

        repository_summary = self.repository.summary()

        return {
            "repository": repository_summary,
        }

    # ========================================================
    # Python Protocol
    # ========================================================

    def __str__(self) -> str:
        return (
            "CanonicalKnowledgeRepositoryBuilder("
            f"{self.summary()}"
            ")"
        )

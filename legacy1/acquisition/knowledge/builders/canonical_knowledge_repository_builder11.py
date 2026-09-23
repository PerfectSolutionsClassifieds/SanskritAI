
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
• Preserve compatibility with lightweight repository test doubles

Architecture
------------

CanonicalLexicon
        │
        ▼
CanonicalKnowledgeRepository
        │
        ├── canonical lexical state
        │
        ▼
lexical_repository adapter
        │
        ▼
CanonicalIndexBuilder
        │
        ├── HeadwordIndex
        ├── LemmaIndex
        ├── ContextIndex
        └── SourceIndex

Important Rule
--------------
CanonicalKnowledgeRepository owns canonical lexical state.

Therefore a full rebuild must clear the composition root's
canonical lexicon state rather than relying exclusively on the
domain lexical adapter.

Version
-------
4.1.0
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
    Ensure that the lexical repository exposes ``all()``.

    The canonical lexical adapter normally provides this operation.
    This helper also supports lightweight repository test doubles
    that expose their lexical data through an ``entries`` mapping.
    """

    all_method = getattr(
        lexical_repository,
        "all",
        None,
    )

    if callable(all_method):
        return lexical_repository

    entries = getattr(
        lexical_repository,
        "entries",
        None,
    )

    if isinstance(
        entries,
        dict,
    ):

        def _all() -> tuple[Any, ...]:
            return tuple(
                entries.values(),
            )

        try:
            setattr(
                lexical_repository,
                "all",
                _all,
            )
        except (
            AttributeError,
            TypeError,
        ):
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
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> CanonicalKnowledgeRepository:
        """
        Completely rebuild the canonical knowledge repository.

        Existing canonical lexical state is removed first.

        The supplied lexicons then become the complete repository
        state, after which all lookup indexes are rebuilt.
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
    def lexical_repository(
        self,
    ) -> Any:
        """
        Return the canonical lexical repository adapter.
        """

        repository = self.repository.lexical_repository

        return _ensure_lexical_repository_has_all(
            repository,
        )

    # ========================================================
    # Population
    # ========================================================

    def _populate_lexical_repository(
        self,
        lexicons: tuple[
            CanonicalLexicon,
            ...,
        ],
    ) -> None:
        """
        Register all supplied lexicons.
        """

        lexical_repository = (
            self.lexical_repository
        )

        for lexicon in lexicons:

            self._register_lexicon(
                lexical_repository,
                lexicon,
            )

    # ========================================================
    # Lexicon Registration
    # ========================================================

    @staticmethod
    def _register_lexicon(
        lexical_repository: Any,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Register one lexicon.

        ``add`` is preferred. Compatibility aliases are retained
        for existing repository implementations and test doubles.
        """

        add = getattr(
            lexical_repository,
            "add",
            None,
        )

        if callable(add):
            add(
                lexicon,
            )
            return

        add_lexicon = getattr(
            lexical_repository,
            "add_lexicon",
            None,
        )

        if callable(add_lexicon):
            add_lexicon(
                lexicon,
            )
            return

        register = getattr(
            lexical_repository,
            "register",
            None,
        )

        if callable(register):
            register(
                lexicon,
            )
            return

        register_lexicon = getattr(
            lexical_repository,
            "register_lexicon",
            None,
        )

        if callable(register_lexicon):
            register_lexicon(
                lexicon,
            )
            return

        raise AttributeError(
            "Canonical lexical repository must provide "
            "one of: 'add', 'add_lexicon', 'register', "
            "or 'register_lexicon'."
        )

    # ========================================================
    # Index Synchronization
    # ========================================================

    def _synchronize_indexes(
        self,
    ) -> None:
        """
        Rebuild all canonical indexes from current repository state.
        """

        lexical_repository = (
            self.lexical_repository
        )

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
        Add one lexicon incrementally.

        Unlike ``build()``, this method intentionally preserves
        existing lexical repository state.
        """

        self._register_lexicon(
            self.lexical_repository,
            lexicon,
        )

        self._synchronize_indexes()

    # ========================================================
    # Maintenance
    # ========================================================

    def clear(
        self,
    ) -> None:
        """
        Clear the canonical repository and all lookup indexes.

        Architectural rule
        ------------------
        CanonicalKnowledgeRepository owns canonical lexical state.

        Therefore ``clear_lexicons()`` is preferred whenever it is
        available. The lexical adapter's ``clear()`` is retained as
        a compatibility fallback for lightweight repository doubles.
        """

        # ----------------------------------------------------
        # Canonical lexical state
        # ----------------------------------------------------

        clear_lexicons = getattr(
            self.repository,
            "clear_lexicons",
            None,
        )

        if callable(clear_lexicons):

            clear_lexicons()

        else:

            # ------------------------------------------------
            # Compatibility fallback
            # ------------------------------------------------

            lexical_repository = (
                self.lexical_repository
            )

            clear = getattr(
                lexical_repository,
                "clear",
                None,
            )

            if callable(clear):
                clear()

        # ----------------------------------------------------
        # Lookup indexes
        # ----------------------------------------------------

        self.index_builder.clear()

    # ========================================================
    # Diagnostics
    # ========================================================

    def summary(
        self,
    ) -> dict:
        """
        Return a compact builder summary.
        """

        repository_summary = self.repository.summary()

        return {
            "repository": repository_summary,
        }

    # ========================================================
    # Representation
    # ========================================================

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalKnowledgeRepositoryBuilder("
            f"{self.summary()}"
            ")"
        )

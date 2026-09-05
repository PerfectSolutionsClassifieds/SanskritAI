
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
• Synchronize all lookup indexes
• Support complete rebuilds
• Support incremental lexicon addition
• Preserve compatibility with lightweight repository test doubles

Architecture
------------

CanonicalLexicon
        │
        ▼
CanonicalKnowledgeRepository
        │
        ├── lexical_repository
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
5.0.0
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
    Ensure that a lexical repository exposes ``all()``.

    The canonical lexical repository already provides this API.

    This helper remains intentionally public-at-module-level
    because lightweight repository test doubles import it
    directly.
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
        Completely rebuild the canonical repository.

        Existing lexical state and index state are discarded
        before the supplied lexicons are registered.
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
        Return the canonical lexical repository.
        """

        lexical_repository = (
            self.repository.lexical_repository
        )

        return _ensure_lexical_repository_has_all(
            lexical_repository,
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
        Register one lexicon using the canonical repository API.

        ``add`` is the preferred operation. Compatibility
        fallbacks support lightweight repository implementations.
        """

        for method_name in (
            "add",
            "add_lexicon",
            "register",
            "register_lexicon",
        ):

            method = getattr(
                lexical_repository,
                method_name,
                None,
            )

            if callable(method):

                method(
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
        Rebuild all lookup indexes from canonical lexical data.
        """

        self.index_builder.build(
            self.lexical_repository.all(),
        )

    # ========================================================
    # Incremental Addition
    # ========================================================

    def add_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Add one lexicon incrementally and rebuild indexes.
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
        Clear repository lexical state and all index state.

        The canonical repository architecture owns lexical data
        through ``lexical_repository``. The old ``lexical_registry``
        attribute must not be referenced here.
        """

        # -----------------------------------------------------
        # Canonical lexical repository
        # -----------------------------------------------------

        lexical_repository = (
            self.lexical_repository
        )

        clear_method = getattr(
            lexical_repository,
            "clear",
            None,
        )

        if callable(clear_method):
            clear_method()

        # -----------------------------------------------------
        # Canonical indexes
        # -----------------------------------------------------

        self.index_builder.clear()

    # ========================================================
    # Diagnostics
    # ========================================================

    def summary(
        self,
    ) -> dict:
        """
        Return builder diagnostics.
        """

        return {
            "repository": self.repository.summary(),
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

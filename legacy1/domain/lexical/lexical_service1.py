from __future__ import annotations

"""
SanskritAI
==========

Lexical Service

Provides the application-facing façade for the Lexical Kernel.

The service coordinates lexical lookup operations while
remaining independent of any particular lexical repository
implementation.

Unlike the repository, the service represents domain behavior
rather than persistence.

Relationship
------------

Application
      │
      ▼
LexicalService
      │
      ▼
LexicalRepository
      │
      ▼
LexicalEntryCollection

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.lexical.lexical_entry import (
    LexicalEntry,
)

from SanskritAI.domain.lexical.lexical_entry_collection import (
    LexicalEntryCollection,
)

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)


@dataclass(frozen=True, slots=True)
class LexicalService(
    Displayable,
):
    """
    Domain façade over the lexical repository.

    Future responsibilities may include:

        • multi-dictionary lookup

        • lexical normalization

        • lexical ranking

        • synonym expansion

        • semantic retrieval

        • lexical caching

        • AI-assisted lexical enrichment

    while keeping clients independent of repository details.
    """

    repository: LexicalRepository

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Lexical Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Domain façade for lexical knowledge retrieval."
        )

    # ---------------------------------------------------------
    # Identity Lookup
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> LexicalEntry | None:
        """
        Retrieves a lexical entry by identifier.
        """

        return self.repository.get(identifier)

    # ---------------------------------------------------------
    # Lemma Lookup
    # ---------------------------------------------------------

    def lookup_lemma(
        self,
        lemma: str,
    ) -> LexicalEntryCollection:
        """
        Retrieves lexical entries for a canonical lemma.
        """

        return self.repository.find_by_lemma(lemma)

    # ---------------------------------------------------------
    # Word-form Lookup
    # ---------------------------------------------------------

    def lookup_word_form(
        self,
        word_form: str,
    ) -> LexicalEntryCollection:
        """
        Retrieves lexical entries matching an inflected form.
        """

        return self.repository.find_by_word_form(word_form)

    # ---------------------------------------------------------
    # Root Lookup
    # ---------------------------------------------------------

    def lookup_root(
        self,
        root: str,
    ) -> LexicalEntryCollection:
        """
        Retrieves lexical entries belonging to a dhātu or
        lexical root.
        """

        return self.repository.find_by_root(root)

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> LexicalEntryCollection:
        """
        Performs lexical search.

        Concrete repositories may support:

            • exact search

            • prefix search

            • fuzzy search

            • semantic search

            • hybrid retrieval
        """

        return self.repository.search(query)

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all_entries(
        self,
    ) -> LexicalEntryCollection:
        """
        Returns every lexical entry.
        """

        return self.repository.all()

    # ---------------------------------------------------------
    # Repository Information
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        """
        Total number of lexical entries.
        """

        return self.repository.count

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether a lexical entry exists.
        """

        return self.repository.contains(identifier)

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text

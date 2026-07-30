from __future__ import annotations

"""
SanskritAI
==========

Lexical Repository

Defines the repository abstraction for the Lexical Kernel.

The repository is responsible for retrieving complete
LexicalEntry aggregate roots from one or more lexical
knowledge sources.

It intentionally contains no implementation details regarding
storage technology (JSON, SQL, PostgreSQL, Neo4j, RDF,
Amarakośa, Wiktionary, etc.).

Relationship
------------

LexicalService
        │
        ▼
LexicalRepository
        │
        ▼
LexicalEntryCollection
        │
        ▼
LexicalEntry

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.lexical.lexical_entry import (
    LexicalEntry,
)

from SanskritAI.domain.lexical.lexical_entry_collection import (
    LexicalEntryCollection,
)


class LexicalRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for lexical knowledge.

    Concrete implementations may retrieve lexical information
    from:

        • Amarakośa

        • Monier-Williams

        • Vācaspatyam

        • Śabdakalpadruma

        • Apte

        • PostgreSQL

        • Graph databases

        • JSON repositories

        • AI semantic indexes

    All implementations return immutable LexicalEntry
    aggregate roots.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Abstract repository for lexical knowledge."
        )

    # ---------------------------------------------------------
    # Identity lookup
    # ---------------------------------------------------------

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> LexicalEntry | None:
        """
        Retrieves a lexical entry by identifier.

        Returns
        -------
        LexicalEntry | None
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Lemma lookup
    # ---------------------------------------------------------

    @abstractmethod
    def find_by_lemma(
        self,
        lemma: str,
    ) -> LexicalEntryCollection:
        """
        Finds lexical entries matching a canonical lemma.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Word-form lookup
    # ---------------------------------------------------------

    @abstractmethod
    def find_by_word_form(
        self,
        word_form: str,
    ) -> LexicalEntryCollection:
        """
        Finds lexical entries matching an inflected word form.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Root lookup
    # ---------------------------------------------------------

    @abstractmethod
    def find_by_root(
        self,
        root: str,
    ) -> LexicalEntryCollection:
        """
        Finds lexical entries belonging to a dhātu or lexical
        root.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Full-text lookup
    # ---------------------------------------------------------

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> LexicalEntryCollection:
        """
        Performs lexical search.

        Concrete implementations may support:

            exact match

            prefix search

            fuzzy search

            semantic search

            hybrid retrieval
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    @abstractmethod
    def all(
        self,
    ) -> LexicalEntryCollection:
        """
        Returns every lexical entry known to the repository.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Existence
    # ---------------------------------------------------------

    @abstractmethod
    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether a lexical entry exists.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Cardinality
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def count(
        self,
    ) -> int:
        """
        Number of lexical entries.
        """

        raise NotImplementedError

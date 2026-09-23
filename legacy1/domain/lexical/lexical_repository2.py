from __future__ import annotations

"""
SanskritAI
==========

Lexical Repository

Adapter over the Canonical Knowledge Repository.

Purpose
-------
The Lexical Kernel no longer owns lexical persistence.

Instead, it delegates all retrieval operations to the
CanonicalKnowledgeRepository, which has become the single
source of truth for Sanskrit lexical knowledge.

Architecture
------------

LexicalService
        │
        ▼
LexicalRepository (Adapter)
        │
        ▼
CanonicalKnowledgeRepository
        │
        ├── Registries
        ├── KnowledgeIndex
        ├── CanonicalLexicons
        ├── CanonicalDictionaryEntries
        ├── CanonicalDictionarySenses
        ├── CanonicalContexts
        └── CanonicalSources

Responsibilities
----------------

• Adapt the Domain Lexical Kernel to the Canonical Repository

• Hide canonical storage implementation

• Preserve a stable interface for LexicalService

Version
-------
v2.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


class LexicalRepository(
    ABC,
    Displayable,
):
    """
    Adapter over CanonicalKnowledgeRepository.

    The Domain layer never accesses indices directly.

    All lexical retrieval is delegated through this adapter.
    """

    def __init__(
        self,
        repository: CanonicalKnowledgeRepository,
    ) -> None:

        self._repository = repository

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
            "Adapter over the Canonical Knowledge Repository."
        )

    # ---------------------------------------------------------
    # Canonical Repository
    # ---------------------------------------------------------

    @property
    def repository(
        self,
    ) -> CanonicalKnowledgeRepository:
        """
        Underlying canonical repository.
        """
        return self._repository

    # ---------------------------------------------------------
    # Identity Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def get_entry(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:
        """
        Retrieves a canonical dictionary entry by headword.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Lemma Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def find_entries_by_lemma(
        self,
        lemma: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Retrieves canonical entries matching a lemma.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Word-form Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def find_entries_by_word_form(
        self,
        word_form: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Retrieves canonical entries matching a surface form.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Sense Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def find_senses(
        self,
        headword: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        """
        Retrieves all senses belonging to a headword.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Performs lexical search.

        Implementations may use:

            • HeadwordIndex

            • LemmaIndex

            • Full-text index

            • Semantic index
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    @abstractmethod
    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Returns every canonical dictionary entry.
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
        Total number of canonical entries.
        """
        raise NotImplementedError

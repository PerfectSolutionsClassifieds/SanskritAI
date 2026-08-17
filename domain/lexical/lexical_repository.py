from __future__ import annotations

"""
SanskritAI
==========

Lexical Repository
------------------

Adapter abstraction between the Domain Lexical Kernel and
the canonical knowledge layer.

Important dependency rule
-------------------------

This module MUST NOT import CanonicalKnowledgeRepository
at runtime.

CanonicalKnowledgeRepository is a composition root which
constructs the domain repositories. Importing the composition
root from this domain abstraction creates:

    CanonicalKnowledgeRepository
        ↓
    KnowledgeServiceRegistry
        ↓
    LexicalRepository
        ↓
    CanonicalKnowledgeRepository

Therefore the CanonicalKnowledgeRepository reference is used
only for static type checking.

Runtime dependency direction:

    Composition Root
          ↓
    LexicalRepository
          ↓
    Canonical knowledge object

Version
-------
v2.0.1
"""

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


if TYPE_CHECKING:
    from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
        CanonicalKnowledgeRepository,
    )


class LexicalRepository(
    ABC,
    Displayable,
):
    """
    Adapter abstraction for canonical lexical knowledge.

    The domain lexical layer communicates through this stable
    interface rather than depending on a concrete storage
    implementation.
    """

    def __init__(
        self,
        repository: CanonicalKnowledgeRepository,
    ) -> None:
        self._repository = repository

    # =========================================================
    # Display
    # =========================================================

    @property
    def display_name(
        self,
    ) -> str:
        return self.__class__.__name__

    @property
    def display_text(
        self,
    ) -> str:
        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Adapter over the Canonical Knowledge Repository."
        )

    # =========================================================
    # Canonical Repository
    # =========================================================

    @property
    def repository(
        self,
    ) -> CanonicalKnowledgeRepository:
        """
        Underlying canonical knowledge object.

        The concrete type is available to static type checkers
        but is deliberately not imported at runtime.
        """

        return self._repository

    # =========================================================
    # Identity Lookup
    # =========================================================

    @abstractmethod
    def get_entry(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:
        """
        Retrieve a canonical dictionary entry by headword.
        """

        raise NotImplementedError

    # =========================================================
    # Lemma Lookup
    # =========================================================

    @abstractmethod
    def find_entries_by_lemma(
        self,
        lemma: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Retrieve canonical entries matching a lemma.
        """

        raise NotImplementedError

    # =========================================================
    # Word-form Lookup
    # =========================================================

    @abstractmethod
    def find_entries_by_word_form(
        self,
        word_form: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Retrieve canonical entries matching a surface form.
        """

        raise NotImplementedError

    # =========================================================
    # Sense Lookup
    # =========================================================

    @abstractmethod
    def find_senses(
        self,
        headword: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        """
        Retrieve all senses belonging to a headword.
        """

        raise NotImplementedError

    # =========================================================
    # Search
    # =========================================================

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Perform lexical search.

        Implementations may use:

            • HeadwordIndex
            • LemmaIndex
            • Full-text index
            • Semantic index
        """

        raise NotImplementedError

    # =========================================================
    # Enumeration
    # =========================================================

    @abstractmethod
    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Return every canonical dictionary entry.
        """

        raise NotImplementedError

    # =========================================================
    # Cardinality
    # =========================================================

    @property
    @abstractmethod
    def count(
        self,
    ) -> int:
        """
        Total number of canonical entries.
        """

        raise NotImplementedError

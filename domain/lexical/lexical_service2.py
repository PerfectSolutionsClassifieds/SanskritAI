from __future__ import annotations

"""
SanskritAI
==========

Lexical Service

Application-facing façade for the Lexical Kernel.

Purpose
-------
Coordinates lexical lookup while remaining independent of the
underlying Canonical Knowledge Repository implementation.

Unlike the repository adapter, this service represents domain
behaviour rather than persistence.

Architecture
------------

Application
      │
      ▼
LexicalService
      │
      ▼
LexicalRepository (Adapter)
      │
      ▼
CanonicalKnowledgeRepository

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LexicalService(
    Displayable,
):
    """
    Domain façade over lexical knowledge.

    Future responsibilities include

        • multi-lexicon lookup

        • lexical normalization

        • ranking

        • semantic expansion

        • AI-assisted enrichment

    while remaining independent of repository internals.
    """

    repository: LexicalRepository

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Lexical Service"

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
            "Domain façade for canonical lexical retrieval."
        )

    # ---------------------------------------------------------
    # Entry Lookup
    # ---------------------------------------------------------

    def get_entry(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:
        """
        Retrieves one canonical dictionary entry.
        """

        return self.repository.get_entry(
            headword,
        )

    # ---------------------------------------------------------
    # Lemma Lookup
    # ---------------------------------------------------------

    def lookup_lemma(
        self,
        lemma: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Retrieves entries matching a canonical lemma.
        """

        return self.repository.find_entries_by_lemma(
            lemma,
        )

    # ---------------------------------------------------------
    # Word-form Lookup
    # ---------------------------------------------------------

    def lookup_word_form(
        self,
        word_form: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Retrieves entries matching a surface form.
        """

        return self.repository.find_entries_by_word_form(
            word_form,
        )

    # ---------------------------------------------------------
    # Sense Lookup
    # ---------------------------------------------------------

    def lookup_senses(
        self,
        headword: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        """
        Retrieves every canonical sense belonging to a headword.
        """

        return self.repository.find_senses(
            headword,
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Performs lexical search.
        """

        return self.repository.search(
            query,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Returns every canonical dictionary entry.
        """

        return self.repository.all_entries()

    # ---------------------------------------------------------
    # Repository Information
    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:
        """
        Total canonical dictionary entries.
        """

        return self.repository.count

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text

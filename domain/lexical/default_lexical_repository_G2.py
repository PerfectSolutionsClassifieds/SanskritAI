from __future__ import annotations

"""
SanskritAI
==========

Default Lexical Repository
--------------------------

Canonical implementation of LexicalRepository.

The repository adapts the canonical knowledge layer to the
Lexical Kernel.

Important dependency rule
-------------------------

CanonicalKnowledgeRepository is a composition root.

Therefore this module must NOT import it at runtime.

The repository reference is used only as a type annotation
and is resolved by static type checkers through TYPE_CHECKING.

Version
-------
v3.0.1
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)


if TYPE_CHECKING:
    from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
        CanonicalKnowledgeRepository,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultLexicalRepository(
    LexicalRepository,
):
    """
    Canonical adapter over the CanonicalKnowledgeRepository.

    The actual repository instance is dependency-injected by
    the composition root.
    """

    repository: CanonicalKnowledgeRepository

    # =========================================================
    # Display
    # =========================================================

    @property
    def display_name(
        self,
    ) -> str:
        return "Default Lexical Repository"

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
            "Canonical adapter exposing lexical knowledge."
        )

    # =========================================================
    # Entry
    # =========================================================

    def get_entry(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:

        return self.repository.get_entry(
            headword,
        )

    # =========================================================
    # Lemma
    # =========================================================

    def find_entries_by_lemma(
        self,
        lemma: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        return self.repository.find_entries_by_lemma(
            lemma,
        )

    # =========================================================
    # Word Form
    # =========================================================

    def find_entries_by_word_form(
        self,
        word_form: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        return self.repository.find_entries_by_word_form(
            word_form,
        )

    # =========================================================
    # Senses
    # =========================================================

    def find_senses(
        self,
        headword: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:

        return self.repository.find_senses(
            headword,
        )

    # =========================================================
    # Search
    # =========================================================

    def search(
        self,
        query: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        return self.repository.search(
            query,
        )

    # =========================================================
    # Enumeration
    # =========================================================

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        return self.repository.all_entries()

    # =========================================================
    # Information
    # =========================================================

    @property
    def count(
        self,
    ) -> int:

        return self.repository.lexical_entry_count

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:
        return self.display_text

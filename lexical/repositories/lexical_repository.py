from __future__ import annotations

"""
SanskritAI
==========

Lexical Repository

Defines the repository contract for accessing lexical knowledge.

A LexicalRepository provides a common interface through which
lexical sources can be queried without exposing their underlying
storage or dictionary-specific representation.

Concrete repositories and adapters may later implement this
contract for:

- Monier-Williams
- Apte
- Amarakośa
- Śabdakalpadruma
- Vācaspatyam

The repository abstraction intentionally separates lexical
domain models from persistence and source-specific data access.

Version
-------
v0.3.0
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexical_source import LexicalSource


class LexicalRepository(ABC):
    """
    Abstract repository contract for lexical knowledge.
    """

    # =========================================================
    # Source
    # =========================================================

    @property
    @abstractmethod
    def source(self) -> LexicalSource:
        """
        Return the lexical source represented by this repository.
        """
        raise NotImplementedError

    # =========================================================
    # Lexeme Lookup
    # =========================================================

    @abstractmethod
    def get_lexeme(
        self,
        identifier: str,
    ) -> Lexeme | None:
        """
        Return a lexeme by identifier.

        Returns None when the lexeme does not exist.
        """
        raise NotImplementedError

    # =========================================================
    # Dictionary Entry Lookup
    # =========================================================

    @abstractmethod
    def get_entry(
        self,
        identifier: str,
    ) -> DictionaryEntry | None:
        """
        Return a dictionary entry by identifier.

        Returns None when the entry does not exist.
        """
        raise NotImplementedError

    # =========================================================
    # Dictionary Sense Lookup
    # =========================================================

    @abstractmethod
    def get_sense(
        self,
        identifier: str,
    ) -> DictionarySense | None:
        """
        Return a dictionary sense by identifier.

        Returns None when the sense does not exist.
        """
        raise NotImplementedError

    # =========================================================
    # Lemma Search
    # =========================================================

    @abstractmethod
    def find_by_lemma(
        self,
        lemma: str,
    ) -> Sequence[Lexeme | DictionaryEntry]:
        """
        Find lexical objects matching a lemma.
        """
        raise NotImplementedError

    # =========================================================
    # Transliteration Search
    # =========================================================

    @abstractmethod
    def find_by_transliteration(
        self,
        transliteration: str,
    ) -> Sequence[Lexeme | DictionaryEntry]:
        """
        Find lexical objects matching a transliteration.
        """
        raise NotImplementedError

    # =========================================================
    # Existence
    # =========================================================

    @abstractmethod
    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True when the repository contains the identifier.
        """
        raise NotImplementedError

    # =========================================================
    # General Search
    # =========================================================

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> Sequence[
        Lexeme | DictionaryEntry | DictionarySense
    ]:
        """
        Perform a general lexical search.
        """
        raise NotImplementedError

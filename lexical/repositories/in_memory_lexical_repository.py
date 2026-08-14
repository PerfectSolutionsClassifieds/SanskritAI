from __future__ import annotations

"""
SanskritAI
==========

In-Memory Lexical Repository

Concrete in-memory implementation of the LexicalRepository
contract.

This repository is intended for:

- unit testing
- development
- prototyping
- deterministic lexical operations
- future adapter validation

It deliberately contains no persistence or dictionary-specific
logic.

Version
-------
v0.3.0
"""

from collections.abc import Sequence

from SanskritAI.lexical.models.dictionary_entry import DictionaryEntry
from SanskritAI.lexical.models.dictionary_sense import DictionarySense
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexical_source import LexicalSource
from SanskritAI.lexical.repositories.lexical_repository import (
    LexicalRepository,
)


class InMemoryLexicalRepository(LexicalRepository):
    """
    In-memory implementation of the lexical repository contract.
    """

    def __init__(
        self,
        source: LexicalSource,
    ) -> None:
        if not isinstance(source, LexicalSource):
            raise TypeError("source must be a LexicalSource.")

        self._source = source
        self._lexemes: dict[str, Lexeme] = {}
        self._entries: dict[str, DictionaryEntry] = {}
        self._senses: dict[str, DictionarySense] = {}

    # =========================================================
    # Source
    # =========================================================

    @property
    def source(self) -> LexicalSource:
        """
        Return the lexical source represented by this repository.
        """
        return self._source

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        lexical_object: (
            Lexeme
            | DictionaryEntry
            | DictionarySense
        ),
    ) -> None:
        """
        Add a lexical object to the repository.
        """
        if isinstance(lexical_object, Lexeme):
            self._lexemes[lexical_object.id] = lexical_object
            return

        if isinstance(lexical_object, DictionaryEntry):
            self._entries[lexical_object.id] = lexical_object
            return

        if isinstance(lexical_object, DictionarySense):
            self._senses[lexical_object.id] = lexical_object
            return

        raise TypeError(
            "lexical_object must be a Lexeme, DictionaryEntry, "
            "or DictionarySense."
        )

    def add_many(
        self,
        lexical_objects: Sequence[
            Lexeme
            | DictionaryEntry
            | DictionarySense
        ],
    ) -> None:
        """
        Add multiple lexical objects.
        """
        for lexical_object in lexical_objects:
            self.add(lexical_object)

    # =========================================================
    # Lexeme Lookup
    # =========================================================

    def get_lexeme(
        self,
        identifier: str,
    ) -> Lexeme | None:
        """
        Return a lexeme by identifier.
        """
        return self._lexemes.get(str(identifier))

    # =========================================================
    # Dictionary Entry Lookup
    # =========================================================

    def get_entry(
        self,
        identifier: str,
    ) -> DictionaryEntry | None:
        """
        Return a dictionary entry by identifier.
        """
        return self._entries.get(str(identifier))

    # =========================================================
    # Dictionary Sense Lookup
    # =========================================================

    def get_sense(
        self,
        identifier: str,
    ) -> DictionarySense | None:
        """
        Return a dictionary sense by identifier.
        """
        return self._senses.get(str(identifier))

    # =========================================================
    # Lemma Search
    # =========================================================

    def find_by_lemma(
        self,
        lemma: str,
    ) -> Sequence[Lexeme | DictionaryEntry]:
        """
        Find lexemes and dictionary entries whose lemma exactly
        matches the supplied value.
        """
        query = str(lemma)

        results: list[Lexeme | DictionaryEntry] = []

        for lexeme in self._lexemes.values():
            if lexeme.metadata.lemma == query:
                results.append(lexeme)

        for entry in self._entries.values():
            if entry.metadata.lemma == query:
                results.append(entry)

        return tuple(results)

    # =========================================================
    # Transliteration Search
    # =========================================================

    def find_by_transliteration(
        self,
        transliteration: str,
    ) -> Sequence[Lexeme | DictionaryEntry]:
        """
        Find lexemes and dictionary entries whose transliteration
        exactly matches the supplied value.
        """
        query = str(transliteration)

        results: list[Lexeme | DictionaryEntry] = []

        for lexeme in self._lexemes.values():
            if lexeme.metadata.transliteration == query:
                results.append(lexeme)

        for entry in self._entries.values():
            if entry.metadata.transliteration == query:
                results.append(entry)

        return tuple(results)

    # =========================================================
    # Existence
    # =========================================================

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True when the identifier exists in the repository.
        """
        key = str(identifier)

        return (
            key in self._lexemes
            or key in self._entries
            or key in self._senses
        )

    # =========================================================
    # General Search
    # =========================================================

    def search(
        self,
        query: str,
    ) -> Sequence[
        Lexeme
        | DictionaryEntry
        | DictionarySense
    ]:
        """
        Perform a simple case-sensitive substring search.

        Searchable fields:

        Lexeme / DictionaryEntry
            - identifier
            - lemma
            - transliteration
            - description

        DictionarySense
            - identifier
            - definition
            - short_definition
            - gloss
        """
        query = str(query)

        results: list[
            Lexeme
            | DictionaryEntry
            | DictionarySense
        ] = []

        for lexeme in self._lexemes.values():
            if self._matches_lexeme(lexeme, query):
                results.append(lexeme)

        for entry in self._entries.values():
            if self._matches_entry(entry, query):
                results.append(entry)

        for sense in self._senses.values():
            if self._matches_sense(sense, query):
                results.append(sense)

        return tuple(results)

    # =========================================================
    # Internal Search Helpers
    # =========================================================

    @staticmethod
    def _matches_lexeme(
        lexeme: Lexeme,
        query: str,
    ) -> bool:
        metadata = lexeme.metadata

        return any(
            query in value
            for value in (
                str(lexeme.id),
                metadata.lemma,
                metadata.transliteration,
                metadata.description,
            )
        )

    @staticmethod
    def _matches_entry(
        entry: DictionaryEntry,
        query: str,
    ) -> bool:
        metadata = entry.metadata

        return any(
            query in value
            for value in (
                str(entry.id),
                metadata.lemma,
                metadata.transliteration,
                metadata.description,
            )
        )

    @staticmethod
    def _matches_sense(
        sense: DictionarySense,
        query: str,
    ) -> bool:
        return any(
            query in value
            for value in (
                str(sense.id),
                sense.definition,
                sense.short_definition,
                sense.gloss,
            )
        )

    # =========================================================
    # Repository State
    # =========================================================

    @property
    def lexeme_count(self) -> int:
        """
        Number of registered lexemes.
        """
        return len(self._lexemes)

    @property
    def entry_count(self) -> int:
        """
        Number of registered dictionary entries.
        """
        return len(self._entries)

    @property
    def sense_count(self) -> int:
        """
        Number of registered dictionary senses.
        """
        return len(self._senses)

    @property
    def count(self) -> int:
        """
        Total number of registered lexical objects.
        """
        return (
            self.lexeme_count
            + self.entry_count
            + self.sense_count
        )

    def clear(self) -> None:
        """
        Remove all lexical objects from the repository.
        """
        self._lexemes.clear()
        self._entries.clear()
        self._senses.clear()

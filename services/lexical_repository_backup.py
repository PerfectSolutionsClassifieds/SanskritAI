"""
SanskritAI
==========

Module:
    services.lexical_repository

Description
-----------
Central repository managing all Lexeme objects.

Responsibilities
----------------
* Global Lexeme registry
* Fast lookup by:
    - Lexeme ID
    - Lemma
    - Transliteration
    - Dictionary source
* Duplicate detection
* Repository statistics
* Future database integration

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from collections import defaultdict

from models.enums.dictionary_source import DictionarySource
from models.lexical import DictionaryEntry
from models.lexical import Lexeme


class LexicalRepository:
    """
    Central repository of all Lexeme objects.

    One instance of this class typically exists for an
    analysis session.

    Future versions may transparently use PostgreSQL,
    MongoDB, Neo4j or Redis without changing the API.
    """

    def __init__(self):

        # -------------------------------------------------
        # Primary index
        # -------------------------------------------------

        self._lexemes: dict[str, Lexeme] = {}

        # -------------------------------------------------
        # Secondary indexes
        # -------------------------------------------------

        self._lemma_index: dict[str, str] = {}

        self._transliteration_index: dict[str, str] = {}

        self._dictionary_index: defaultdict[
            DictionarySource,
            dict[str, str]
        ] = defaultdict(dict)

    # =====================================================
    # Registration
    # =====================================================

    def add(self, lexeme: Lexeme) -> None:
        """
        Register a Lexeme.

        Existing IDs are replaced.
        """

        self._lexemes[lexeme.lexeme_id] = lexeme

        self._lemma_index[
            lexeme.lemma
        ] = lexeme.lexeme_id

        if lexeme.transliteration:

            self._transliteration_index[
                lexeme.transliteration
            ] = lexeme.lexeme_id

        for entry in lexeme.dictionary_entries:

            self._dictionary_index[
                entry.source
            ][entry.headword] = lexeme.lexeme_id

    # =====================================================
    # Removal
    # =====================================================

    def remove(
        self,
        lexeme_id: str
    ) -> bool:

        lexeme = self._lexemes.pop(
            lexeme_id,
            None,
        )

        if lexeme is None:
            return False

        self._lemma_index.pop(
            lexeme.lemma,
            None,
        )

        self._transliteration_index.pop(
            lexeme.transliteration,
            None,
        )

        for entry in lexeme.dictionary_entries:

            self._dictionary_index[
                entry.source
            ].pop(
                entry.headword,
                None,
            )

        return True

    # =====================================================
    # Lookup
    # =====================================================

    def get(
        self,
        lexeme_id: str
    ) -> Lexeme | None:

        return self._lexemes.get(lexeme_id)

    def by_lemma(
        self,
        lemma: str
    ) -> Lexeme | None:

        lexeme_id = self._lemma_index.get(lemma)

        if lexeme_id is None:
            return None

        return self._lexemes[lexeme_id]

    def by_transliteration(
        self,
        transliteration: str
    ) -> Lexeme | None:

        lexeme_id = self._transliteration_index.get(
            transliteration
        )

        if lexeme_id is None:
            return None

        return self._lexemes[lexeme_id]

    def by_dictionary(
        self,
        source: DictionarySource,
        headword: str,
    ) -> Lexeme | None:

        lexeme_id = self._dictionary_index[
            source
        ].get(headword)

        if lexeme_id is None:
            return None

        return self._lexemes[lexeme_id]

    # =====================================================
    # Queries
    # =====================================================

    def contains(
        self,
        lexeme_id: str
    ) -> bool:

        return lexeme_id in self._lexemes

    def all(self) -> list[Lexeme]:

        return list(self._lexemes.values())

    def clear(self):

        self._lexemes.clear()

        self._lemma_index.clear()

        self._transliteration_index.clear()

        self._dictionary_index.clear()

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def lexeme_count(self) -> int:

        return len(self._lexemes)

    @property
    def dictionary_sources(
        self,
    ) -> list[DictionarySource]:

        return list(
            self._dictionary_index.keys()
        )

    # =====================================================
    # Import helpers
    # =====================================================

    def add_dictionary_entry(
        self,
        lexeme_id: str,
        entry: DictionaryEntry,
    ) -> None:
        """
        Attach a dictionary entry to an existing Lexeme.

        Repository indexes are automatically updated.
        """

        lexeme = self.get(lexeme_id)

        if lexeme is None:
            raise KeyError(
                f"Unknown Lexeme: {lexeme_id}"
            )

        lexeme.add_dictionary_entry(entry)

        self._dictionary_index[
            entry.source
        ][entry.headword] = lexeme.lexeme_id

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {

            "lexeme_count": self.lexeme_count,

            "lexemes": [

                lexeme.to_dict()

                for lexeme in self.all()

            ]
        }

    # =====================================================
    # Representation
    # =====================================================

    def __len__(self):

        return self.lexeme_count

    def __iter__(self):

        return iter(self.all())

    def __repr__(self):

        return (
            f"LexicalRepository("
            f"lexemes={self.lexeme_count})"
        )

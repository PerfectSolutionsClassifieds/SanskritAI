"""
SanskritAI
==========

Module:
    services.repositories.memory_lexical_repository

Description
-----------
Default in-memory implementation of the lexical repository.

This implementation is optimized for development, unit testing,
Google Colab, and small to medium corpora.

Future implementations may store identical objects in PostgreSQL,
Neo4j, MongoDB, Redis, etc. without changing the public API.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from models.enums.dictionary_source import DictionarySource
from models.lexical import DictionaryEntry
from models.lexical import Lexeme

from .lexical_repository_base import LexicalRepositoryBase


class MemoryLexicalRepository(LexicalRepositoryBase):
    """
    Default in-memory implementation of the lexical repository.

    Multiple secondary indexes provide O(1) lookup by:

        • Lexeme ID
        • Lemma
        • Transliteration
        • Dictionary source + headword
    """

    def __init__(self) -> None:

        # ---------------------------------------------------------
        # Primary Storage
        # ---------------------------------------------------------

        self._lexemes: dict[str, Lexeme] = {}

        # ---------------------------------------------------------
        # Secondary Indexes
        # ---------------------------------------------------------

        self._lemma_index: dict[str, str] = {}

        self._transliteration_index: dict[str, str] = {}

        self._dictionary_index: defaultdict[
            DictionarySource,
            dict[str, str],
        ] = defaultdict(dict)

    # =========================================================
    # Internal Index Management
    # =========================================================

    def _index_lexeme(
        self,
        lexeme: Lexeme,
    ) -> None:
        """
        Register all secondary indexes for a Lexeme.
        """

        if lexeme.lemma in self._lemma_index:
            raise ValueError(
                f"Duplicate lemma '{lexeme.lemma}'."
            )

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

    def _deindex_lexeme(
        self,
        lexeme: Lexeme,
    ) -> None:
        """
        Remove all secondary indexes for a Lexeme.
        """

        self._lemma_index.pop(
            lexeme.lemma,
            None,
        )

        if lexeme.transliteration:

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

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        lexeme: Lexeme,
    ) -> None:
        """
        Add a new Lexeme.

        Raises
        ------
        KeyError
            If the Lexeme ID already exists.
        """

        if self.exists(lexeme.lexeme_id):
            raise KeyError(
                f"Lexeme '{lexeme.lexeme_id}' already exists."
            )

        self._lexemes[
            lexeme.lexeme_id
        ] = lexeme

        self._index_lexeme(lexeme)

    def update(
        self,
        lexeme: Lexeme,
    ) -> None:
        """
        Replace an existing Lexeme.

        Secondary indexes are rebuilt automatically.
        """

        if not self.exists(lexeme.lexeme_id):
            raise KeyError(
                f"Unknown Lexeme '{lexeme.lexeme_id}'."
            )

        old = self._lexemes[
            lexeme.lexeme_id
        ]

        self._deindex_lexeme(old)

        self._lexemes[
            lexeme.lexeme_id
        ] = lexeme

        self._index_lexeme(lexeme)

    # =========================================================
    # Removal
    # =========================================================

    def remove(
        self,
        lexeme_id: str,
    ) -> bool:
        """
        Remove one Lexeme.
        """

        lexeme = self._lexemes.pop(
            lexeme_id,
            None,
        )

        if lexeme is None:
            return False

        self._deindex_lexeme(lexeme)

        return True
        #############################
    # =========================================================
    # Lookup
    # =========================================================

    def get(
        self,
        lexeme_id: str,
    ) -> Lexeme | None:
        """
        Retrieve a Lexeme by its unique ID.
        """

        return self._lexemes.get(lexeme_id)

    def by_lemma(
        self,
        lemma: str,
    ) -> Lexeme | None:
        """
        Retrieve a Lexeme by its canonical lemma.
        """

        lexeme_id = self._lemma_index.get(lemma)

        if lexeme_id is None:
            return None

        return self._lexemes[lexeme_id]

    def by_transliteration(
        self,
        transliteration: str,
    ) -> Lexeme | None:
        """
        Retrieve a Lexeme by transliteration.
        """

        lexeme_id = self._transliteration_index.get(
            transliteration
        )

        if lexeme_id is None:
            return None

        return self._lexemes[lexeme_id]

    def find_by_dictionary(
        self,
        source: DictionarySource,
        headword: str,
    ) -> Lexeme | None:
        """
        Retrieve a Lexeme using a dictionary source and headword.
        """

        lexeme_id = self._dictionary_index[
            source
        ].get(headword)

        if lexeme_id is None:
            return None

        return self._lexemes[lexeme_id]

    # =========================================================
    # Dictionary Operations
    # =========================================================

    def add_dictionary_entry(
        self,
        lexeme_id: str,
        entry: DictionaryEntry,
    ) -> None:
        """
        Attach a DictionaryEntry to an existing Lexeme.
        """

        lexeme = self.get(lexeme_id)

        if lexeme is None:
            raise KeyError(
                f"Unknown Lexeme '{lexeme_id}'."
            )

        old_entry = lexeme.get_entry(entry.source)

        if old_entry is not None:

            self._dictionary_index[
                old_entry.source
            ].pop(
                old_entry.headword,
                None,
            )

        lexeme.add_dictionary_entry(entry)

        self._dictionary_index[
            entry.source
        ][entry.headword] = lexeme.lexeme_id

    # =========================================================
    # Repository Operations
    # =========================================================

    def exists(
        self,
        lexeme_id: str,
    ) -> bool:
        """
        Return True if the Lexeme exists.
        """

        return lexeme_id in self._lexemes

    def all(
        self,
    ) -> tuple[Lexeme, ...]:
        """
        Return all stored Lexeme objects.

        Returns an immutable tuple.
        """

        return tuple(self._lexemes.values())

    def clear(self) -> None:
        """
        Remove all stored Lexeme objects.
        """

        self._lexemes.clear()

        self._lemma_index.clear()

        self._transliteration_index.clear()

        self._dictionary_index.clear()

    # =========================================================
    # Properties
    # =========================================================

    @property
    def dictionary_sources(
        self,
    ) -> tuple[DictionarySource, ...]:
        """
        Available dictionary sources currently indexed.
        """

        return tuple(
            sorted(
                self._dictionary_index.keys(),
                key=lambda source: source.value,
            )
        )

    # =========================================================
    # Serialization
    # =========================================================

    def to_dict(self) -> dict:
        """
        Serialize the repository.
        """

        return {

            "lexeme_count": len(self),

            "lexemes": [

                lexeme.to_dict()

                for lexeme in self

            ],

        }

    # =========================================================
    # Python Protocols
    # =========================================================

    def __iter__(
        self,
    ) -> Iterator[Lexeme]:
        """
        Iterate over stored Lexeme objects.
        """

        return iter(self.all())

    def __len__(
        self,
    ) -> int:
        """
        Number of stored Lexeme objects.
        """

        return len(self._lexemes)

    def __contains__(
        self,
        lexeme_id: str,
    ) -> bool:
        """
        Membership test.

        Example
        -------
        if "LEX0001" in repository:
            ...
        """

        return self.exists(lexeme_id)

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(
        self,
    ) -> str:

        return (
            "MemoryLexicalRepository("
            f"lexemes={len(self)}, "
            f"dictionary_sources={len(self.dictionary_sources)})"
        )    

"""
SanskritAI
==========

Module:
    services.repositories.lexical_repository_base

Description:
    Abstract repository interface for managing Lexeme objects.

    All lexical storage implementations (memory, JSON,
    PostgreSQL, Neo4j, MongoDB, etc.) must implement this API.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterator

from models.enums.dictionary_source import DictionarySource
from models.lexical import DictionaryEntry
from models.lexical import Lexeme


class LexicalRepositoryBase(ABC):
    """
    Abstract storage contract for Lexeme repositories.

    Concrete implementations may use:

        • In-memory
        • JSON
        • SQLite
        • PostgreSQL
        • MongoDB
        • Neo4j

    Analysis engines communicate ONLY through this interface.
    """

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    @abstractmethod
    def add(
        self,
        lexeme: Lexeme,
    ) -> None:
        """Add a new Lexeme."""
        ...

    @abstractmethod
    def update(
        self,
        lexeme: Lexeme,
    ) -> None:
        """Update an existing Lexeme."""
        ...

    @abstractmethod
    def remove(
        self,
        lexeme_id: str,
    ) -> bool:
        """Remove a Lexeme by ID."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove all Lexeme objects."""
        ...

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    @abstractmethod
    def get(
        self,
        lexeme_id: str,
    ) -> Lexeme | None:
        """Retrieve a Lexeme by ID."""
        ...

    @abstractmethod
    def by_lemma(
        self,
        lemma: str,
    ) -> Lexeme | None:
        """Retrieve by canonical lemma."""
        ...

    @abstractmethod
    def by_transliteration(
        self,
        transliteration: str,
    ) -> Lexeme | None:
        """Retrieve by transliteration."""
        ...

    @abstractmethod
    def find_by_dictionary(
        self,
        source: DictionarySource,
        headword: str,
    ) -> Lexeme | None:
        """Retrieve by dictionary source and headword."""
        ...

    # ---------------------------------------------------------
    # Dictionary Operations
    # ---------------------------------------------------------

    @abstractmethod
    def add_dictionary_entry(
        self,
        lexeme_id: str,
        entry: DictionaryEntry,
    ) -> None:
        """Attach a DictionaryEntry to an existing Lexeme."""
        ...

    # ---------------------------------------------------------
    # Repository Operations
    # ---------------------------------------------------------

    @abstractmethod
    def exists(
        self,
        lexeme_id: str,
    ) -> bool:
        """Return True if the Lexeme exists."""
        ...

    @abstractmethod
    def all(self) -> tuple[Lexeme, ...]:
        """
        Return all Lexeme objects.

        Implementations should return an immutable tuple.
        """
        ...

    # ---------------------------------------------------------
    # Python Protocols
    # ---------------------------------------------------------

    @abstractmethod
    def __iter__(self) -> Iterator[Lexeme]:
        """Iterate over stored Lexeme objects."""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Number of stored Lexeme objects."""
        ...

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def lexeme_count(self) -> int:
        """Number of stored Lexeme objects."""
        return len(self)

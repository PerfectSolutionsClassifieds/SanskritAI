"""
SanskritAI
==========

Module:
    models.imports.import_statistics

Description
-----------
Collects statistics produced during an import operation.

This class is generic and reusable by every importer within
SanskritAI.

Examples
--------
    Amarakośa Importer

    Purāṇa Importer

    Veda Importer

    Dictionary Importer

    JSON Importer

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter


@dataclass(slots=True)
class ImportStatistics:
    """
    Statistics collected during an import operation.
    """

    # ---------------------------------------------------------
    # Structural Objects
    # ---------------------------------------------------------

    books: int = 0

    kandas: int = 0

    vargas: int = 0

    chapters: int = 0

    sections: int = 0

    verses: int = 0

    # ---------------------------------------------------------
    # Lexical Objects
    # ---------------------------------------------------------

    tokens: int = 0

    lexemes: int = 0

    dictionary_entries: int = 0

    dictionary_senses: int = 0

    lexical_relations: int = 0

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    warnings: int = 0

    errors: int = 0

    skipped: int = 0

    duplicates: int = 0

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    started_at: float = 0.0

    finished_at: float = 0.0

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def start(self) -> None:
        """
        Start timing.
        """

        self.started_at = perf_counter()

    def stop(self) -> None:
        """
        Stop timing.
        """

        self.finished_at = perf_counter()

    # ---------------------------------------------------------
    # Timing Properties
    # ---------------------------------------------------------

    @property
    def elapsed_seconds(self) -> float:

        if self.started_at == 0.0:
            return 0.0

        if self.finished_at == 0.0:
            return perf_counter() - self.started_at

        return self.finished_at - self.started_at

    # ---------------------------------------------------------
    # Convenience Counters
    # ---------------------------------------------------------

    @property
    def imported_objects(self) -> int:
        """
        Total imported domain objects.
        """

        return (
            self.books
            + self.kandas
            + self.vargas
            + self.chapters
            + self.sections
            + self.verses
        )

    @property
    def lexical_objects(self) -> int:
        """
        Total lexical objects produced.
        """

        return (
            self.lexemes
            + self.dictionary_entries
            + self.dictionary_senses
            + self.lexical_relations
        )

    @property
    def has_errors(self) -> bool:

        return self.errors > 0

    @property
    def has_warnings(self) -> bool:

        return self.warnings > 0

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset all counters.
        """

        self.books = 0

        self.kandas = 0

        self.vargas = 0

        self.chapters = 0

        self.sections = 0

        self.verses = 0

        self.tokens = 0

        self.lexemes = 0

        self.dictionary_entries = 0

        self.dictionary_senses = 0

        self.lexical_relations = 0

        self.warnings = 0

        self.errors = 0

        self.skipped = 0

        self.duplicates = 0

        self.started_at = 0.0

        self.finished_at = 0.0

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "books": self.books,

            "kandas": self.kandas,

            "vargas": self.vargas,

            "chapters": self.chapters,

            "sections": self.sections,

            "verses": self.verses,

            "tokens": self.tokens,

            "lexemes": self.lexemes,

            "dictionary_entries": self.dictionary_entries,

            "dictionary_senses": self.dictionary_senses,

            "lexical_relations": self.lexical_relations,

            "warnings": self.warnings,

            "errors": self.errors,

            "skipped": self.skipped,

            "duplicates": self.duplicates,

            "elapsed_seconds": round(
                self.elapsed_seconds,
                3,
            ),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return (
            f"Imported {self.imported_objects} objects "
            f"({self.lexemes} lexemes)"
        )

    def __repr__(self) -> str:

        return (
            "ImportStatistics("
            f"objects={self.imported_objects}, "
            f"lexemes={self.lexemes}, "
            f"errors={self.errors}, "
            f"warnings={self.warnings})"
        )

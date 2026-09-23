
"""
SanskritAI
==========

Module:
    services.importers.import_result_builder

Description
-----------
Immutability factory layer for assembling full unified ImportResult objects 
upon processing completion.

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations
from models.amarakosha import Amarakosha
from models.imports import ImportResult, ImportStatistics, ImportError, ImportStatus


class ImportResultBuilder:
    """
    Assembles and seals final output records for consumer systems.
    Defends against partial mutate actions downstream.
    """

    def __init__(self) -> None:
        self._status: ImportStatus = ImportStatus.FAILED
        self._book: Amarakosha = Amarakosha()
        self._statistics: ImportStatistics = ImportStatistics()
        self._errors: list[ImportError] = []

    def with_status(self, status: ImportStatus) -> ImportResultBuilder:
        self._status = status
        return self

    def with_book(self, book: Amarakosha) -> ImportResultBuilder:
        self._book = book
        return self

    def with_statistics(self, statistics: ImportStatistics) -> ImportResultBuilder:
        self._statistics = statistics
        return self

    def with_errors(self, errors: list[ImportError]) -> ImportResultBuilder:
        self._errors = list(errors)
        return self

    def build(self) -> ImportResult:
        """Constructs an immutable production-ready ImportResult snapshot."""
        return ImportResult(
            status=self._status,
            book=self._book,
            statistics=self._statistics,
            errors=self._errors
        )

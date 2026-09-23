"""
SanskritAI
==========

Module:
    services.importers.import_result_builder

Description
-----------
Builder for assembling canonical ImportResult objects.

The builder is intentionally independent of a specific imported
domain object. Amarakośa, Purāṇa, Veda, dictionary and future
importers may all use the same result-building contract.

Compatibility
-------------
``with_book()`` is retained as a compatibility alias for the
Amarakośa importer. New code should prefer ``with_imported_object()``.

Version
-------
v0.9.0
"""

from __future__ import annotations

from typing import Any, Self

from SanskritAI.models.imports import (
    ImportError,
    ImportResult,
    ImportStatistics,
    ImportStatus,
)


class ImportResultBuilder:
    """
    Builder for canonical ImportResult objects.

    The builder assembles a result snapshot without introducing
    importer-specific result models.
    """

    # =========================================================
    # Construction
    # =========================================================

    def __init__(self) -> None:

        self._status = ImportStatus.PENDING

        self._importer_name = ""

        self._source_file = None

        self._message: str | None = None

        self._imported_object: Any | None = None

        self._imported_documents: list[str] = []

        self._imported_units: list[str] = []

        self._skipped_units: list[str] = []

        self._statistics = ImportStatistics()

        self._errors: list[ImportError] = []

        self._metadata: dict[str, Any] = {}

    # =========================================================
    # Lifecycle
    # =========================================================

    def with_status(
        self,
        status: ImportStatus,
    ) -> Self:

        self._status = status

        return self

    # =========================================================
    # Identity
    # =========================================================

    def with_importer_name(
        self,
        importer_name: str,
    ) -> Self:

        self._importer_name = importer_name

        return self

    # =========================================================

    def with_source_file(
        self,
        source_file,
    ) -> Self:

        self._source_file = source_file

        return self

    # =========================================================

    def with_message(
        self,
        message: str | None,
    ) -> Self:

        self._message = message

        return self

    # =========================================================
    # Domain Object
    # =========================================================

    def with_imported_object(
        self,
        imported_object: Any,
    ) -> Self:

        self._imported_object = imported_object

        return self

    # =========================================================
    # Amarakośa Compatibility
    # =========================================================

    def with_book(
        self,
        book: Any,
    ) -> Self:
        """
        Compatibility alias for Amarakośa import code.

        New code should use ``with_imported_object()``.
        """

        return self.with_imported_object(
            book
        )

    # =========================================================
    # Acquisition Tracking
    # =========================================================

    def with_imported_documents(
        self,
        documents: list[str],
    ) -> Self:

        self._imported_documents = list(
            documents
        )

        return self

    # =========================================================

    def with_imported_units(
        self,
        units: list[str],
    ) -> Self:

        self._imported_units = list(
            units
        )

        return self

    # =========================================================

    def with_skipped_units(
        self,
        units: list[str],
    ) -> Self:

        self._skipped_units = list(
            units
        )

        return self

    # =========================================================
    # Statistics
    # =========================================================

    def with_statistics(
        self,
        statistics: ImportStatistics,
    ) -> Self:

        self._statistics = statistics

        return self

    # =========================================================
    # Diagnostics
    # =========================================================

    def with_errors(
        self,
        errors: list[ImportError],
    ) -> Self:

        self._errors = list(
            errors
        )

        return self

    # =========================================================
    # Metadata
    # =========================================================

    def with_metadata(
        self,
        metadata: dict[str, Any],
    ) -> Self:

        self._metadata = dict(
            metadata
        )

        return self

    # =========================================================
    # Build
    # =========================================================

    def build(
        self,
    ) -> ImportResult:
        """
        Construct the canonical ImportResult.

        The supplied statistics and diagnostics are copied into
        the result so that the builder retains no ownership of
        the resulting mutable collections.
        """

        result = ImportResult(

            status=self._status,

            importer_name=self._importer_name,

            source_file=self._source_file,

            message=self._message,

            imported_object=self._imported_object,

            imported_documents=list(
                self._imported_documents
            ),

            imported_units=list(
                self._imported_units
            ),

            skipped_units=list(
                self._skipped_units
            ),

            statistics=self._statistics,

            errors=list(
                self._errors
            ),

            metadata=dict(
                self._metadata
            ),
        )

        return result

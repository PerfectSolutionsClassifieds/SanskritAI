"""
SanskritAI
==========

Module:
    models.imports.import_result

Description
-----------
Represents the outcome of an import operation.

Every importer returns exactly one ImportResult object,
regardless of whether the import succeeds or fails.

ImportResult aggregates:

    • Import status
    • Imported domain object
    • Statistics
    • Errors
    • Metadata

This class is intentionally generic and reusable across all
future SanskritAI importers.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .import_error import ImportError
from .import_statistics import ImportStatistics
from .import_status import ImportStatus


@dataclass(slots=True)
class ImportResult:
    """
    Result of an import operation.

    The imported_object may be any domain model.

    Examples
    --------

    Amarakośa Importer
        imported_object -> Amarakosha

    Purāṇa Importer
        imported_object -> Purana

    Dictionary Importer
        imported_object -> list[Lexeme]
    """

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    status: ImportStatus = ImportStatus.PENDING

    # ---------------------------------------------------------
    # Imported Object
    # ---------------------------------------------------------

    imported_object: Any | None = None

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    statistics: ImportStatistics = field(
        default_factory=ImportStatistics
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    errors: list[ImportError] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def add_error(
        self,
        error: ImportError,
    ) -> None:
        """
        Register one import error.
        """

        self.errors.append(error)

        if error.is_warning:

            self.statistics.warnings += 1

        elif error.is_error:

            self.statistics.errors += 1

        elif error.is_fatal:

            self.statistics.errors += 1

            self.status = ImportStatus.FAILED

    # ---------------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    # ---------------------------------------------------------

    @property
    def warning_count(self) -> int:

        return self.statistics.warnings

    @property
    def error_count(self) -> int:

        return self.statistics.errors

    @property
    def has_errors(self) -> bool:

        return self.error_count > 0

    @property
    def has_warnings(self) -> bool:

        return self.warning_count > 0

    @property
    def successful(self) -> bool:

        return self.status.is_success

    # ---------------------------------------------------------
    # Finalization
    # ---------------------------------------------------------

    def finalize(self) -> None:
        """
        Determine the final import status.

        Called by an importer after processing has completed.
        """

        if self.status == ImportStatus.FAILED:
            return

        if self.statistics.errors > 0:

            self.status = ImportStatus.FAILED

        elif self.statistics.warnings > 0:

            self.status = (
                ImportStatus.COMPLETED_WITH_WARNINGS
            )

        else:

            self.status = ImportStatus.COMPLETED

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "status": self.status.value,

            "statistics": self.statistics.to_dict(),

            "errors": [

                error.to_dict()

                for error in self.errors

            ],

            "metadata": self.metadata,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return (
            f"{self.status.value} "
            f"(errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )

    def __repr__(self) -> str:

        return (
            "ImportResult("
            f"status={self.status.name}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )


from __future__ import annotations

"""
SanskritAI
==========

Import Result

Defines the standardized result object returned by every importer
within the Acquisition Import Pipeline.

An ImportResult represents the outcome of importing a single resource
or a batch of resources into the canonical SanskritAI corpus.

Responsibilities
----------------
* Imported document tracking
* Imported unit tracking
* Warning collection
* Error collection
* Import statistics
* Timing information
* Metadata

Every concrete importer (TXT, XML, TEI, HTML, PDF, etc.) returns
an ImportResult so the ImportManager remains format-independent.

Version
-------
v0.8.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ImportResult:
    """
    Standardized importer result.
    """

    # ---------------------------------------------------------
    # Import Status
    # ---------------------------------------------------------

    importer_name: str

    source_file: Path

    success: bool = True

    message: str | None = None

    # ---------------------------------------------------------
    # Imported Objects
    # ---------------------------------------------------------

    imported_documents: list[str] = field(
        default_factory=list
    )

    imported_units: list[str] = field(
        default_factory=list
    )

    skipped_units: list[str] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    started_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    finished_at: datetime | None = None

    # ---------------------------------------------------------
    # Imported Documents
    # ---------------------------------------------------------

    def add_document(
        self,
        identifier: str,
    ) -> None:

        if identifier not in self.imported_documents:

            self.imported_documents.append(
                identifier
            )

    # ---------------------------------------------------------

    def add_unit(
        self,
        identifier: str,
    ) -> None:

        self.imported_units.append(
            identifier
        )

    # ---------------------------------------------------------

    def skip_unit(
        self,
        identifier: str,
    ) -> None:

        self.skipped_units.append(
            identifier
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(
            message
        )

    # ---------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> None:

        self.errors.append(
            message
        )

        self.success = False

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    # ---------------------------------------------------------

    def increment(
        self,
        key: str,
        amount: int = 1,
    ) -> None:

        self.statistics[key] = (

            self.statistics.get(
                key,
                0,
            )

            + amount

        )

    # ---------------------------------------------------------
    # Completion
    # ---------------------------------------------------------

    def finish(
        self,
    ) -> None:

        self.finished_at = datetime.now(
            timezone.utc
        )

        self.statistics.setdefault(
            "documents_imported",
            len(self.imported_documents),
        )

        self.statistics.setdefault(
            "units_imported",
            len(self.imported_units),
        )

        self.statistics.setdefault(
            "units_skipped",
            len(self.skipped_units),
        )

        self.statistics.setdefault(
            "warning_count",
            len(self.warnings),
        )

        self.statistics.setdefault(
            "error_count",
            len(self.errors),
        )

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def duration_seconds(
        self,
    ) -> float | None:

        if self.finished_at is None:

            return None

        return (

            self.finished_at

            - self.started_at

        ).total_seconds()

    # ---------------------------------------------------------

    @property
    def document_count(
        self,
    ) -> int:

        return len(
            self.imported_documents
        )

    # ---------------------------------------------------------

    @property
    def unit_count(
        self,
    ) -> int:

        return len(
            self.imported_units
        )

    # ---------------------------------------------------------

    @property
    def has_errors(
        self,
    ) -> bool:

        return bool(
            self.errors
        )

    # ---------------------------------------------------------

    @property
    def has_warnings(
        self,
    ) -> bool:

        return bool(
            self.warnings
        )

    # ---------------------------------------------------------

    def merge(
        self,
        other: "ImportResult",
    ) -> None:
        """
        Merge another ImportResult into this one.

        Used by ImportManager when importing multiple files.
        """

        for document in other.imported_documents:

            if document not in self.imported_documents:

                self.imported_documents.append(
                    document
                )

        self.imported_units.extend(
            other.imported_units
        )

        self.skipped_units.extend(
            other.skipped_units
        )

        self.warnings.extend(
            other.warnings
        )

        self.errors.extend(
            other.errors
        )

        self.metadata.update(
            other.metadata
        )

        for key, value in other.statistics.items():

            if isinstance(value, int):

                self.statistics[key] = (

                    self.statistics.get(
                        key,
                        0,
                    )

                    + value

                )

            else:

                self.statistics[key] = value

        self.success = (

            self.success

            and other.success

        )

    # ---------------------------------------------------------

    def __bool__(
        self,
    ) -> bool:

        return self.success

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.unit_count

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "ImportResult("

            f"importer={self.importer_name!r}, "

            f"file={self.source_file.name!r}, "

            f"documents={self.document_count}, "

            f"units={self.unit_count}, "

            f"errors={len(self.errors)})"

        )

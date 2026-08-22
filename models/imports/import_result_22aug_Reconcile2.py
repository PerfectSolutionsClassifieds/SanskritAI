"""
SanskritAI
==========

Module:
    models.imports.import_result

Description
-----------
Canonical result object for every SanskritAI import operation.

ImportResult is the single unified result contract shared by:

    • Acquisition importers
    • Service-level importers
    • Corpus import pipelines
    • Dictionary importers
    • Amarakośa importers
    • Purāṇa importers
    • Vedic importers
    • Future import pipelines

The result combines:

    • Import lifecycle status
    • Imported domain object
    • Imported document/unit tracking
    • Import statistics
    • Structured diagnostics
    • Metadata
    • Source/importer identity

Architecture
------------

    Importer
        │
        ▼
    ImportResult
        │
        ├── status
        ├── imported_object
        ├── statistics
        ├── errors
        ├── metadata
        └── source information

ImportResult represents the outcome of an operation.
It does not own canonical corpus identity.

Canonical identity remains the responsibility of:

    CorpusId
    DocumentId
    SectionId
    VerseId
    ...

Version
-------
v0.9.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .import_error import ImportError
from .import_statistics import ImportStatistics
from .import_status import ImportStatus


@dataclass(slots=True)
class ImportResult:
    """
    Canonical result of an import operation.

    Parameters
    ----------
    status:
        Current lifecycle status.

    imported_object:
        Domain object produced by the import operation.

    importer_name:
        Human-readable importer identity.

    source_file:
        Optional source file associated with the operation.

    Examples
    --------
    Amarakośa:

        imported_object -> Amarakosha

    Purāṇa:

        imported_object -> Purana

    Dictionary:

        imported_object -> list[Lexeme]
    """

    # =========================================================
    # Lifecycle
    # =========================================================

    status: ImportStatus = ImportStatus.PENDING

    # =========================================================
    # Importer Identity
    # =========================================================

    importer_name: str = ""

    source_file: Path | None = None

    message: str | None = None

    # =========================================================
    # Imported Domain Object
    # =========================================================

    imported_object: Any | None = None

    # =========================================================
    # Acquisition Tracking
    # =========================================================

    imported_documents: list[str] = field(
        default_factory=list
    )

    imported_units: list[str] = field(
        default_factory=list
    )

    skipped_units: list[str] = field(
        default_factory=list
    )

    # =========================================================
    # Statistics
    # =========================================================

    statistics: ImportStatistics = field(
        default_factory=ImportStatistics
    )

    # =========================================================
    # Diagnostics
    # =========================================================

    errors: list[ImportError] = field(
        default_factory=list
    )

    # =========================================================
    # Metadata
    # =========================================================

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # Lifecycle Initialization
    # =========================================================

    def __post_init__(self) -> None:
        """
        Start the import statistics timer.

        A result created for an already completed operation can
        subsequently be finalized immediately.
        """

        if self.statistics.started_at == 0.0:
            self.statistics.start()

    # =========================================================
    # Imported Documents
    # =========================================================

    def add_document(
        self,
        identifier: str,
    ) -> None:
        """
        Register one imported document.

        Duplicate document identifiers are ignored.
        """

        identifier = identifier.strip()

        if not identifier:
            return

        if identifier not in self.imported_documents:

            self.imported_documents.append(
                identifier
            )

    # =========================================================

    def add_unit(
        self,
        identifier: str,
    ) -> None:
        """
        Register one imported unit.
        """

        identifier = identifier.strip()

        if identifier:
            self.imported_units.append(
                identifier
            )

    # =========================================================

    def skip_unit(
        self,
        identifier: str,
    ) -> None:
        """
        Register one skipped unit.
        """

        identifier = identifier.strip()

        if identifier:
            self.skipped_units.append(
                identifier
            )

        self.statistics.skipped += 1

    # =========================================================
    # Diagnostics
    # =========================================================

    def add_error(
        self,
        error: ImportError,
    ) -> None:
        """
        Register a structured import diagnostic.

        Severity controls the corresponding statistics counter
        and lifecycle status.
        """

        self.errors.append(error)

        if error.is_info:
            return

        if error.is_warning:

            self.statistics.warnings += 1

            return

        if error.is_error:

            self.statistics.errors += 1

            return

        if error.is_fatal:

            self.statistics.errors += 1

            self.status = ImportStatus.FAILED

    # =========================================================

    def warning(
        self,
        message: str,
        *,
        file_name: str = "",
        line_number: int | None = None,
        column_number: int | None = None,
        error_type: str = "",
        context: str = "",
    ) -> None:
        """
        Register a warning using the structured diagnostic model.
        """

        self.add_error(
            ImportError(
                message=message,
                file_name=file_name,
                line_number=line_number,
                column_number=column_number,
                severity="WARNING",
                error_type=error_type,
                context=context,
            )
        )

    # =========================================================

    def error(
        self,
        message: str,
        *,
        file_name: str = "",
        line_number: int | None = None,
        column_number: int | None = None,
        error_type: str = "",
        context: str = "",
        exception: str = "",
        fatal: bool = False,
    ) -> None:
        """
        Register an error using the structured diagnostic model.
        """

        self.add_error(
            ImportError(
                message=message,
                file_name=file_name,
                line_number=line_number,
                column_number=column_number,
                severity=(
                    "FATAL"
                    if fatal
                    else "ERROR"
                ),
                error_type=error_type,
                context=context,
                exception=exception,
            )
        )

    # =========================================================
    # Metadata
    # =========================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add or replace one metadata value.
        """

        self.metadata[key] = value

    # =========================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Compatibility alias for add_metadata().
        """

        self.add_metadata(
            key,
            value,
        )

    # =========================================================
    # Statistics
    # =========================================================

    def increment(
        self,
        key: str,
        amount: int = 1,
    ) -> None:
        """
        Increment a named ImportStatistics counter.

        Only existing numeric statistics fields are accepted.
        """

        if not hasattr(
            self.statistics,
            key,
        ):
            raise AttributeError(
                f"Unknown ImportStatistics field: {key}"
            )

        value = getattr(
            self.statistics,
            key,
        )

        if not isinstance(value, int):
            raise TypeError(
                f"ImportStatistics.{key} "
                f"is not an integer counter."
            )

        setattr(
            self.statistics,
            key,
            value + amount,
        )

    # =========================================================
    # Convenience Properties
    # =========================================================

    @property
    def warning_count(self) -> int:
        return self.statistics.warnings

    # =========================================================

    @property
    def error_count(self) -> int:
        return self.statistics.errors

    # =========================================================

    @property
    def has_errors(self) -> bool:
        return self.statistics.errors > 0

    # =========================================================

    @property
    def has_warnings(self) -> bool:
        return self.statistics.warnings > 0

    # =========================================================

    @property
    def successful(self) -> bool:
        return self.status.is_success

    # =========================================================

    @property
    def duration_seconds(self) -> float:
        return self.statistics.elapsed_seconds

    # =========================================================

    @property
    def document_count(self) -> int:
        return len(
            self.imported_documents
        )

    # =========================================================

    @property
    def unit_count(self) -> int:
        return len(
            self.imported_units
        )

    # =========================================================
    # Finalization
    # =========================================================

    def finalize(self) -> None:
        """
        Finalize the import lifecycle.

        Existing FAILED/CANCELLED states are preserved.
        Otherwise errors and warnings determine the final state.
        """

        if self.status in {
            ImportStatus.FAILED,
            ImportStatus.CANCELLED,
        }:
            self.statistics.stop()
            return

        if self.statistics.errors > 0:

            self.status = ImportStatus.FAILED

        elif self.statistics.warnings > 0:

            self.status = (
                ImportStatus.COMPLETED_WITH_WARNINGS
            )

        else:

            self.status = ImportStatus.COMPLETED

        self.statistics.stop()

    # =========================================================

    def finish(self) -> None:
        """
        Compatibility alias used by acquisition importers.
        """

        self.finalize()

    # =========================================================
    # Merge
    # =========================================================

    def merge(
        self,
        other: "ImportResult",
    ) -> None:
        """
        Merge another ImportResult into this result.

        Used by ImportManager for batch and directory imports.
        """

        # -----------------------------------------------------
        # Documents
        # -----------------------------------------------------

        for document in other.imported_documents:

            self.add_document(
                document
            )

        # -----------------------------------------------------
        # Units
        # -----------------------------------------------------

        self.imported_units.extend(
            other.imported_units
        )

        self.skipped_units.extend(
            other.skipped_units
        )

        # -----------------------------------------------------
        # Diagnostics
        # -----------------------------------------------------

        self.errors.extend(
            other.errors
        )

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        self.metadata.update(
            other.metadata
        )

        # -----------------------------------------------------
        # Statistics
        # -----------------------------------------------------

        self.statistics.books += (
            other.statistics.books
        )

        self.statistics.kandas += (
            other.statistics.kandas
        )

        self.statistics.vargas += (
            other.statistics.vargas
        )

        self.statistics.chapters += (
            other.statistics.chapters
        )

        self.statistics.sections += (
            other.statistics.sections
        )

        self.statistics.verses += (
            other.statistics.verses
        )

        self.statistics.tokens += (
            other.statistics.tokens
        )

        self.statistics.lexemes += (
            other.statistics.lexemes
        )

        self.statistics.dictionary_entries += (
            other.statistics.dictionary_entries
        )

        self.statistics.dictionary_senses += (
            other.statistics.dictionary_senses
        )

        self.statistics.lexical_relations += (
            other.statistics.lexical_relations
        )

        self.statistics.warnings += (
            other.statistics.warnings
        )

        self.statistics.errors += (
            other.statistics.errors
        )

        self.statistics.skipped += (
            other.statistics.skipped
        )

        self.statistics.duplicates += (
            other.statistics.duplicates
        )

        # -----------------------------------------------------
        # Lifecycle
        # -----------------------------------------------------

        if other.status is ImportStatus.FAILED:

            self.status = ImportStatus.FAILED

        elif (
            other.status
            is ImportStatus.CANCELLED
        ):

            self.status = ImportStatus.CANCELLED

        elif (
            other.status
            is ImportStatus.COMPLETED_WITH_WARNINGS
            and self.status
            not in {
                ImportStatus.FAILED,
                ImportStatus.CANCELLED,
            }
        ):

            self.status = (
                ImportStatus.COMPLETED_WITH_WARNINGS
            )

    # =========================================================
    # Serialization
    # =========================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the complete result.
        """

        return {

            "status":
                self.status.value,

            "importer_name":
                self.importer_name,

            "source_file":
                (
                    str(self.source_file)
                    if self.source_file is not None
                    else None
                ),

            "message":
                self.message,

            "imported_documents":
                list(self.imported_documents),

            "imported_units":
                list(self.imported_units),

            "skipped_units":
                list(self.skipped_units),

            "statistics":
                self.statistics.to_dict(),

            "errors": [
                error.to_dict()
                for error in self.errors
            ],

            "metadata":
                dict(self.metadata),

        }

    # =========================================================
    # Python Protocols
    # =========================================================

    def __bool__(self) -> bool:
        return self.successful

    # =========================================================

    def __len__(self) -> int:
        return self.unit_count

    # =========================================================

    def __str__(self) -> str:

        return (
            f"{self.status.value} "
            f"(errors={self.error_count}, "
            f"warnings={self.warning_count}, "
            f"units={self.unit_count})"
        )

    # =========================================================

    def __repr__(self) -> str:

        return (
            "ImportResult("
            f"status={self.status.name}, "
            f"importer={self.importer_name!r}, "
            f"file={self.source_file!r}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )

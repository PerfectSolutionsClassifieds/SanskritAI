"""
SanskritAI
==========

Module:
    models.imports.import_error

Description
-----------
Represents one warning or error encountered during an import
operation.

ImportError objects are collected inside ImportResult and provide
structured diagnostic information for parsers, importers, and
validation routines.

This model is generic and reusable across all SanskritAI importers.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ImportError:
    """
    Represents one import warning or error.

    Examples
    --------

    Missing verse number

    Invalid Unicode sequence

    Duplicate Lexeme ID

    Unknown DictionarySource

    Unexpected end of file
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    message: str

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    file_name: str = ""

    line_number: int | None = None

    column_number: int | None = None

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    severity: str = "ERROR"
    # INFO | WARNING | ERROR | FATAL

    error_type: str = ""

    # ---------------------------------------------------------
    # Additional Context
    # ---------------------------------------------------------

    context: str = ""

    exception: str = ""

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        self.message = self.message.strip()

        if not self.message:
            raise ValueError(
                "message cannot be empty."
            )

        self.severity = self.severity.upper()

        allowed = {
            "INFO",
            "WARNING",
            "ERROR",
            "FATAL",
        }

        if self.severity not in allowed:
            raise ValueError(
                f"Unknown severity '{self.severity}'."
            )

        if self.line_number is not None:

            if self.line_number < 1:
                raise ValueError(
                    "line_number must be positive."
                )

        if self.column_number is not None:

            if self.column_number < 1:
                raise ValueError(
                    "column_number must be positive."
                )

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def is_info(self) -> bool:

        return self.severity == "INFO"

    @property
    def is_warning(self) -> bool:

        return self.severity == "WARNING"

    @property
    def is_error(self) -> bool:

        return self.severity == "ERROR"

    @property
    def is_fatal(self) -> bool:

        return self.severity == "FATAL"

    @property
    def location(self) -> str:
        """
        Human-readable location string.
        """

        if self.line_number is None:
            return ""

        if self.column_number is None:
            return f"Line {self.line_number}"

        return (
            f"Line {self.line_number}, "
            f"Column {self.column_number}"
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "message": self.message,

            "file_name": self.file_name,

            "line_number": self.line_number,

            "column_number": self.column_number,

            "severity": self.severity,

            "error_type": self.error_type,

            "context": self.context,

            "exception": self.exception,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        location = self.location

        if location:

            return (
                f"[{self.severity}] "
                f"{location}: "
                f"{self.message}"
            )

        return (
            f"[{self.severity}] "
            f"{self.message}"
        )

    def __repr__(self) -> str:

        return (
            "ImportError("
            f"severity='{self.severity}', "
            f"message='{self.message}')"
        )

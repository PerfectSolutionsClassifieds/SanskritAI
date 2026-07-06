"""
SanskritAI
==========

Module:
    models.imports.import_status

Description
-----------
Enumeration representing the lifecycle of an import operation.

Every importer in SanskritAI reports its current status using
this enumeration.

The same status values are applicable to:

    • Amarakośa Importer
    • Purāṇa Importers
    • Vedic Importers
    • Dictionary Importers
    • Lexical Importers
    • Future corpus importers

Version:
    v0.4.0
"""

from __future__ import annotations

from enum import Enum


class ImportStatus(Enum):
    """
    Standard import lifecycle.

    Typical progression::

        PENDING
            ↓
        RUNNING
            ↓
        COMPLETED

    or

        PENDING
            ↓
        RUNNING
            ↓
        COMPLETED_WITH_WARNINGS

    or

        PENDING
            ↓
        RUNNING
            ↓
        FAILED

    or

        PENDING
            ↓
        CANCELLED
    """

    # ---------------------------------------------------------
    # Initial State
    # ---------------------------------------------------------

    PENDING = "Pending"

    # ---------------------------------------------------------
    # Active
    # ---------------------------------------------------------

    RUNNING = "Running"

    # ---------------------------------------------------------
    # Successful
    # ---------------------------------------------------------

    COMPLETED = "Completed"

    COMPLETED_WITH_WARNINGS = "Completed with Warnings"

    # ---------------------------------------------------------
    # Unsuccessful
    # ---------------------------------------------------------

    FAILED = "Failed"

    CANCELLED = "Cancelled"

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def is_finished(self) -> bool:
        """
        True if the import has reached a terminal state.
        """

        return self in {
            ImportStatus.COMPLETED,
            ImportStatus.COMPLETED_WITH_WARNINGS,
            ImportStatus.FAILED,
            ImportStatus.CANCELLED,
        }

    @property
    def is_success(self) -> bool:
        """
        True if the import completed successfully.
        """

        return self in {
            ImportStatus.COMPLETED,
            ImportStatus.COMPLETED_WITH_WARNINGS,
        }

    @property
    def is_failure(self) -> bool:
        """
        True if the import did not complete successfully.
        """

        return self in {
            ImportStatus.FAILED,
            ImportStatus.CANCELLED,
        }

    @property
    def has_warnings(self) -> bool:
        """
        True if the import completed with warnings.
        """

        return self is ImportStatus.COMPLETED_WITH_WARNINGS

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.value

    def __repr__(self) -> str:

        return f"ImportStatus.{self.name}"


from __future__ import annotations

"""
SanskritAI
==========

Acquisition Source Status

Defines the lifecycle state of a corpus source as it moves
through the acquisition pipeline.

The acquisition lifecycle is intentionally independent of
the source type (Corpus, Lexicon, Grammar, etc.) and its
physical format (TXT, XML, PDF, TEI, ...).

Typical Lifecycle
-----------------

REGISTERED
      ↓
DISCOVERED
      ↓
PENDING_DOWNLOAD
      ↓
DOWNLOADING
      ↓
DOWNLOADED
      ↓
VALIDATING
      ↓
VALIDATED
      ↓
NORMALIZING
      ↓
NORMALIZED
      ↓
READY_FOR_IMPORT
      ↓
IMPORTED
      ↓
COMPLETED

Any stage may transition to FAILED.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from enum import Enum


class SourceStatus(str, Enum):
    """
    Lifecycle state of an acquisition source.
    """

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    REGISTERED = "registered"

    DISCOVERED = "discovered"

    # ------------------------------------------------------------------
    # Download
    # ------------------------------------------------------------------

    PENDING_DOWNLOAD = "pending_download"

    DOWNLOADING = "downloading"

    DOWNLOADED = "downloaded"

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    VALIDATING = "validating"

    VALIDATED = "validated"

    # ------------------------------------------------------------------
    # Normalization
    # ------------------------------------------------------------------

    NORMALIZING = "normalizing"

    NORMALIZED = "normalized"

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------

    READY_FOR_IMPORT = "ready_for_import"

    IMPORTING = "importing"

    IMPORTED = "imported"

    # ------------------------------------------------------------------
    # Completion
    # ------------------------------------------------------------------

    COMPLETED = "completed"

    ARCHIVED = "archived"

    # ------------------------------------------------------------------
    # Failure
    # ------------------------------------------------------------------

    FAILED = "failed"

    SKIPPED = "skipped"

    UNKNOWN = "unknown"

    # ==============================================================
    # Convenience Properties
    # ==============================================================

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if the source has reached
        a terminal state.
        """
        return self in {
            SourceStatus.COMPLETED,
            SourceStatus.ARCHIVED,
            SourceStatus.FAILED,
            SourceStatus.SKIPPED,
        }

    @property
    def is_downloaded(self) -> bool:
        """
        Returns True if the source has already
        been downloaded.
        """
        return self in {
            SourceStatus.DOWNLOADED,
            SourceStatus.VALIDATING,
            SourceStatus.VALIDATED,
            SourceStatus.NORMALIZING,
            SourceStatus.NORMALIZED,
            SourceStatus.READY_FOR_IMPORT,
            SourceStatus.IMPORTING,
            SourceStatus.IMPORTED,
            SourceStatus.COMPLETED,
            SourceStatus.ARCHIVED,
        }

    @property
    def is_validated(self) -> bool:
        """
        Returns True if validation has completed.
        """
        return self in {
            SourceStatus.VALIDATED,
            SourceStatus.NORMALIZING,
            SourceStatus.NORMALIZED,
            SourceStatus.READY_FOR_IMPORT,
            SourceStatus.IMPORTING,
            SourceStatus.IMPORTED,
            SourceStatus.COMPLETED,
            SourceStatus.ARCHIVED,
        }

    @property
    def is_importable(self) -> bool:
        """
        Returns True if the source is ready
        for the importer.
        """
        return self in {
            SourceStatus.READY_FOR_IMPORT,
            SourceStatus.IMPORTING,
            SourceStatus.IMPORTED,
            SourceStatus.COMPLETED,
        }

    @property
    def has_failed(self) -> bool:
        """
        Returns True if acquisition failed.
        """
        return self == SourceStatus.FAILED

    @property
    def is_active(self) -> bool:
        """
        Returns True if the source is currently
        undergoing processing.
        """
        return self in {
            SourceStatus.DOWNLOADING,
            SourceStatus.VALIDATING,
            SourceStatus.NORMALIZING,
            SourceStatus.IMPORTING,
        }

    # ==============================================================
    # Factory
    # ==============================================================

    @classmethod
    def from_string(cls, value: str) -> "SourceStatus":
        """
        Parse a string into a SourceStatus.

        Unknown values return UNKNOWN.
        """
        normalized = value.strip().lower()

        for member in cls:
            if member.value == normalized:
                return member

        return cls.UNKNOWN

    # ==============================================================
    # Representation
    # ==============================================================

    def __str__(self) -> str:
        return self.value


from __future__ import annotations

"""
SanskritAI
==========

Acquisition Result

Represents the outcome of a corpus acquisition operation.

This class is intentionally independent of any particular
downloader, validator, or importer. It provides a common
result object that can be returned throughout the acquisition
pipeline.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.models.corpus_source import CorpusSource


@dataclass(slots=True)
class AcquisitionResult:
    """
    Result of an acquisition operation.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    source: CorpusSource

    # ------------------------------------------------------------------
    # Overall Result
    # ------------------------------------------------------------------

    success: bool = True

    message: str = ""

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------

    started_at: datetime = field(default_factory=datetime.utcnow)

    completed_at: datetime | None = None

    duration_seconds: float | None = None

    # ------------------------------------------------------------------
    # Download Information
    # ------------------------------------------------------------------

    downloaded_files: list[Path] = field(default_factory=list)

    extracted_files: list[Path] = field(default_factory=list)

    bytes_downloaded: int = 0

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    checksum_verified: bool = False

    license_verified: bool = False

    normalized: bool = False

    imported: bool = False

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Completion
    # ------------------------------------------------------------------

    def finalize(self) -> None:
        """
        Marks the acquisition as completed.
        """
        self.completed_at = datetime.utcnow()

        self.duration_seconds = (
            self.completed_at - self.started_at
        ).total_seconds()

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def add_warning(self, message: str) -> None:
        """
        Records a warning.
        """
        message = message.strip()

        if message:
            self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """
        Records an error and marks the result as failed.
        """
        message = message.strip()

        if not message:
            return

        self.errors.append(message)
        self.success = False

    # ------------------------------------------------------------------
    # Files
    # ------------------------------------------------------------------

    def add_downloaded_file(
        self,
        path: str | Path,
    ) -> None:
        """
        Registers a downloaded file.
        """
        self.downloaded_files.append(Path(path))

    def add_extracted_file(
        self,
        path: str | Path,
    ) -> None:
        """
        Registers an extracted file.
        """
        self.extracted_files.append(Path(path))

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Stores arbitrary metadata.
        """
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves metadata.
        """
        return self.metadata.get(key, default)

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def downloaded_file_count(self) -> int:
        return len(self.downloaded_files)

    @property
    def extracted_file_count(self) -> int:
        return len(self.extracted_files)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the acquisition result.
        """
        return {
            "source_id": self.source.source_id,
            "success": self.success,
            "message": self.message,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            ),
            "duration_seconds": self.duration_seconds,
            "downloaded_files": [
                str(path)
                for path in self.downloaded_files
            ],
            "extracted_files": [
                str(path)
                for path in self.extracted_files
            ],
            "bytes_downloaded": self.bytes_downloaded,
            "checksum_verified": self.checksum_verified,
            "license_verified": self.license_verified,
            "normalized": self.normalized,
            "imported": self.imported,
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "metadata": dict(self.metadata),
        }

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"AcquisitionResult("
            f"source={self.source.source_id!r}, "
            f"success={self.success}, "
            f"downloads={len(self.downloaded_files)}, "
            f"errors={len(self.errors)})"
        )

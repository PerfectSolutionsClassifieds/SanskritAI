
from __future__ import annotations

"""
SanskritAI
==========

Extraction Result

Standardized result object returned by every metadata extractor.

Responsibilities
----------------
* Store extracted metadata
* Record extractor identity
* Report confidence
* Capture warnings and errors
* Record execution statistics

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from dataclasses import dataclass, field
from typing import Any
import time


@dataclass(slots=True)
class ExtractionResult:
    """
    Result returned by a metadata extractor.
    """

    #
    # Identity
    #

    extractor_name: str

    #
    # Extracted metadata
    #

    metadata: dict[str, Any] = field(default_factory=dict)

    #
    # Diagnostics
    #

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    #
    # Confidence
    #

    confidence: float = 1.0

    #
    # Timing
    #

    started_at: float = field(default_factory=time.perf_counter)

    finished_at: float | None = None

    #
    # Statistics
    #

    statistics: dict[str, Any] = field(default_factory=dict)

    #
    # Provenance
    #

    provenance: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def finish(self) -> None:
        """
        Mark extraction as completed.
        """

        if self.finished_at is None:
            self.finished_at = time.perf_counter()

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def succeeded(self) -> bool:
        """
        True if extraction completed without errors.
        """

        return len(self.errors) == 0

    @property
    def failed(self) -> bool:
        """
        True if extraction produced errors.
        """

        return not self.succeeded

    @property
    def has_warnings(self) -> bool:
        """
        True if warnings were produced.
        """

        return bool(self.warnings)

    @property
    def duration_seconds(self) -> float | None:
        """
        Extraction duration.
        """

        if self.finished_at is None:
            return None

        return self.finished_at - self.started_at

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add or update metadata.
        """

        self.metadata[key] = value

    def merge_metadata(
        self,
        metadata: dict[str, Any],
    ) -> None:
        """
        Merge another metadata dictionary.
        """

        self.metadata.update(metadata)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)

    def add_error(
        self,
        message: str,
    ) -> None:

        self.errors.append(message)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def increment_statistic(
        self,
        key: str,
        amount: int = 1,
    ) -> None:
        """
        Increment a numeric statistic.
        """

        self.statistics[key] = (
            self.statistics.get(key, 0)
            + amount
        )

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    def add_provenance(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Record provenance information.
        """

        self.provenance[key] = value

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to a serializable dictionary.
        """

        return {
            "extractor_name": self.extractor_name,
            "metadata": dict(self.metadata),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "confidence": self.confidence,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "statistics": dict(self.statistics),
            "provenance": dict(self.provenance),
            "succeeded": self.succeeded,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "ExtractionResult("
            f"extractor='{self.extractor_name}', "
            f"metadata={len(self.metadata)}, "
            f"warnings={len(self.warnings)}, "
            f"errors={len(self.errors)}, "
            f"confidence={self.confidence:.2f})"
        )

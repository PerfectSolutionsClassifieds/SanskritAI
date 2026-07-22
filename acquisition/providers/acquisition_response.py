
from __future__ import annotations

"""
SanskritAI
==========

Acquisition Response

Defines the standardized response object returned by every
AcquisitionProvider.

The response represents the complete outcome of an acquisition
operation, including:

    • discovered resources
    • downloaded resources
    • skipped resources
    • failures
    • warnings
    • provider metadata
    • execution statistics

Every provider must return an AcquisitionResponse, allowing the
orchestration layer to remain provider-independent.

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AcquisitionResponse:
    """
    Standardized provider response.
    """

    # ---------------------------------------------------------
    # Provider Information
    # ---------------------------------------------------------

    provider_name: str

    success: bool = True

    message: str | None = None

    # ---------------------------------------------------------
    # Resource Collections
    # ---------------------------------------------------------

    discovered_resources: list[str] = field(
        default_factory=list,
    )

    downloaded_files: list[Path] = field(
        default_factory=list,
    )

    skipped_resources: list[str] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    warnings: list[str] = field(
        default_factory=list,
    )

    errors: list[str] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    statistics: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    started_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    finished_at: datetime | None = None

    # ---------------------------------------------------------
    # Resource API
    # ---------------------------------------------------------

    def add_resource(
        self,
        resource: str,
    ) -> None:
        """
        Register a discovered resource.
        """

        if resource not in self.discovered_resources:

            self.discovered_resources.append(resource)

    # ---------------------------------------------------------

    def add_download(
        self,
        file: Path,
    ) -> None:
        """
        Register a downloaded file.
        """

        if file not in self.downloaded_files:

            self.downloaded_files.append(file)

    # ---------------------------------------------------------

    def skip(
        self,
        resource: str,
    ) -> None:
        """
        Register a skipped resource.
        """

        self.skipped_resources.append(resource)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)

    # ---------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> None:

        self.errors.append(message)

        self.success = False

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
        name: str,
        amount: int = 1,
    ) -> None:

        self.statistics[name] = (

            self.statistics.get(name, 0)

            + amount

        )

    # ---------------------------------------------------------

    def finish(
        self,
    ) -> None:
        """
        Finalize the response.
        """

        self.finished_at = datetime.now(
            timezone.utc
        )

        self.statistics.setdefault(

            "resources_discovered",

            len(self.discovered_resources),

        )

        self.statistics.setdefault(

            "resources_downloaded",

            len(self.downloaded_files),

        )

        self.statistics.setdefault(

            "resources_skipped",

            len(self.skipped_resources),

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
    def has_errors(
        self,
    ) -> bool:

        return bool(self.errors)

    # ---------------------------------------------------------

    @property
    def has_warnings(
        self,
    ) -> bool:

        return bool(self.warnings)

    # ---------------------------------------------------------

    @property
    def resource_count(
        self,
    ) -> int:

        return len(self.discovered_resources)

    # ---------------------------------------------------------

    @property
    def download_count(
        self,
    ) -> int:

        return len(self.downloaded_files)

    # ---------------------------------------------------------

    def merge(
        self,
        other: "AcquisitionResponse",
    ) -> None:
        """
        Merge another provider response into this one.
        Useful for multi-provider orchestration.
        """

        self.discovered_resources.extend(

            resource

            for resource in other.discovered_resources

            if resource not in self.discovered_resources

        )

        self.downloaded_files.extend(

            file

            for file in other.downloaded_files

            if file not in self.downloaded_files

        )

        self.skipped_resources.extend(
            other.skipped_resources
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

                    self.statistics.get(key, 0)

                    + value

                )

            else:

                self.statistics[key] = value

        self.success = (

            self.success

            and other.success

        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.resource_count

    # ---------------------------------------------------------

    def __bool__(
        self,
    ) -> bool:

        return self.success

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "AcquisitionResponse("

            f"provider={self.provider_name!r}, "

            f"success={self.success}, "

            f"resources={self.resource_count}, "

            f"downloads={self.download_count}, "

            f"errors={len(self.errors)})"

        )

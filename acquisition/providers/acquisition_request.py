
from __future__ import annotations

"""
SanskritAI
==========

Acquisition Request

Defines the immutable request object passed to every AcquisitionProvider.

The AcquisitionRequest encapsulates all information required for a
provider to discover and/or acquire one or more corpus resources,
independent of the provider implementation.

Typical Flow
------------
DiscoveryManager
        │
        ▼
 AcquisitionRequest
        │
        ▼
   GRETIL Provider
        │
        ▼
AcquisitionResponse

This object is intentionally provider-agnostic so that every provider
shares the same API.

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class AcquisitionRequest:
    """
    Immutable request describing a corpus acquisition operation.
    """

    # ---------------------------------------------------------
    # Resource Selection
    # ---------------------------------------------------------

    source_identifier: str | None = None
    """
    Canonical source identifier.

    Examples
    --------
    gretil
    cologne
    sarit
    github
    """

    work_identifier: str | None = None
    """
    Canonical work identifier.

    Example
    -------
    srimad_bhagavatam
    """

    query: str | None = None
    """
    Optional free-text query used by searchable repositories.
    """

    # ---------------------------------------------------------
    # Destination
    # ---------------------------------------------------------

    destination_directory: Path | None = None
    """
    Local destination where acquired resources are written.
    """

    overwrite: bool = False

    create_directory: bool = True

    # ---------------------------------------------------------
    # Discovery Options
    # ---------------------------------------------------------

    recursive: bool = True

    include_metadata: bool = True

    include_checksums: bool = True

    include_license: bool = True

    # ---------------------------------------------------------
    # Download Options
    # ---------------------------------------------------------

    download_resources: bool = True

    verify_download: bool = True

    normalize_after_download: bool = False

    extract_archives: bool = True

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    allowed_extensions: tuple[str, ...] = field(
        default_factory=tuple,
    )

    excluded_extensions: tuple[str, ...] = field(
        default_factory=tuple,
    )

    maximum_file_size_mb: int | None = None

    # ---------------------------------------------------------
    # Provider Configuration
    # ---------------------------------------------------------

    provider_options: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Runtime Metadata
    # ---------------------------------------------------------

    request_metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    @property
    def has_query(self) -> bool:

        return bool(
            self.query and self.query.strip()
        )

    # ---------------------------------------------------------

    @property
    def has_work_identifier(self) -> bool:

        return self.work_identifier is not None

    # ---------------------------------------------------------

    @property
    def has_destination(self) -> bool:

        return self.destination_directory is not None

    # ---------------------------------------------------------

    def allows_extension(
        self,
        extension: str,
    ) -> bool:
        """
        Determines whether a file extension is accepted.

        Parameters
        ----------
        extension:
            File extension including or excluding '.'.

        Examples
        --------
        ".xml"
        "txt"
        """

        extension = extension.lower()

        if not extension.startswith("."):

            extension = "." + extension

        if self.allowed_extensions:

            if extension not in {

                ext.lower()
                if ext.startswith(".")
                else "." + ext.lower()

                for ext in self.allowed_extensions
            }:

                return False

        if self.excluded_extensions:

            if extension in {

                ext.lower()
                if ext.startswith(".")
                else "." + ext.lower()

                for ext in self.excluded_extensions
            }:

                return False

        return True

    # ---------------------------------------------------------

    def option(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves a provider-specific option.
        """

        return self.provider_options.get(
            name,
            default,
        )

    # ---------------------------------------------------------

    def metadata(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves request metadata.
        """

        return self.request_metadata.get(
            name,
            default,
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "AcquisitionRequest("
            f"source={self.source_identifier!r}, "
            f"work={self.work_identifier!r}, "
            f"query={self.query!r}, "
            f"download={self.download_resources}, "
            f"destination={self.destination_directory!r})"
        )

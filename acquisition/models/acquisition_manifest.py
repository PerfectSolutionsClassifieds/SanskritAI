
from __future__ import annotations

"""
SanskritAI
==========

Acquisition Manifest

Defines an executable acquisition plan for obtaining a specific
edition or distribution of a corpus source.

A CorpusSource represents the identity of a source.

An AcquisitionManifest represents HOW that source should be
acquired.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat


@dataclass(slots=True)
class AcquisitionManifest:
    """
    Executable acquisition description.

    A single CorpusSource may have multiple manifests.

    Examples
    --------
    Amarakośa
        - Cologne XML
        - GRETIL TXT
        - Local PDF Scan

    Bhagavad Gītā
        - GRETIL
        - SARIT
        - Local OCR Edition
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    manifest_id: str

    source: CorpusSource

    # ------------------------------------------------------------------
    # Acquisition
    # ------------------------------------------------------------------

    urls: list[str] = field(default_factory=list)

    mirrors: list[str] = field(default_factory=list)

    preferred_format: SourceFormat = SourceFormat.UNKNOWN

    # ------------------------------------------------------------------
    # Expected Files
    # ------------------------------------------------------------------

    expected_filename: str | None = None

    expected_size: int | None = None

    checksum: str | None = None

    checksum_algorithm: str = "sha256"

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------

    destination_directory: Path | None = None

    cache_directory: Path | None = None

    overwrite_existing: bool = False

    extract_archives: bool = True

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    importer: str | None = None

    encoding: str = "utf-8"

    normalize_unicode: bool = True

    validate_checksum: bool = True

    validate_license: bool = True

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    priority: int = 100

    enabled: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # URL Management
    # ------------------------------------------------------------------

    def add_url(self, url: str) -> None:
        """
        Adds a primary acquisition URL.
        """
        url = url.strip()

        if url and url not in self.urls:
            self.urls.append(url)

    def add_mirror(self, url: str) -> None:
        """
        Adds a mirror download location.
        """
        url = url.strip()

        if url and url not in self.mirrors:
            self.mirrors.append(url)

    @property
    def all_urls(self) -> list[str]:
        """
        Returns primary URLs followed by mirrors.
        """
        return [
            *self.urls,
            *self.mirrors,
        ]

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Stores arbitrary manifest metadata.
        """
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves manifest metadata.
        """
        return self.metadata.get(key, default)

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    @property
    def has_urls(self) -> bool:
        """
        Returns True if at least one acquisition URL exists.
        """
        return bool(self.all_urls)

    @property
    def requires_download(self) -> bool:
        """
        Returns True if acquisition requires downloading.
        """
        return self.has_urls

    @property
    def requires_checksum_validation(self) -> bool:
        """
        Returns True if checksum validation is enabled.
        """
        return (
            self.validate_checksum
            and self.checksum is not None
        )

    @property
    def requires_license_validation(self) -> bool:
        """
        Returns True if license validation is enabled.
        """
        return self.validate_license

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the manifest into a JSON-safe dictionary.
        """

        return {
            "manifest_id": self.manifest_id,
            "source_id": self.source.source_id,
            "urls": list(self.urls),
            "mirrors": list(self.mirrors),
            "preferred_format": str(self.preferred_format),
            "expected_filename": self.expected_filename,
            "expected_size": self.expected_size,
            "checksum": self.checksum,
            "checksum_algorithm": self.checksum_algorithm,
            "destination_directory": (
                str(self.destination_directory)
                if self.destination_directory
                else None
            ),
            "cache_directory": (
                str(self.cache_directory)
                if self.cache_directory
                else None
            ),
            "overwrite_existing": self.overwrite_existing,
            "extract_archives": self.extract_archives,
            "importer": self.importer,
            "encoding": self.encoding,
            "normalize_unicode": self.normalize_unicode,
            "validate_checksum": self.validate_checksum,
            "validate_license": self.validate_license,
            "priority": self.priority,
            "enabled": self.enabled,
            "metadata": dict(self.metadata),
        }

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"AcquisitionManifest("
            f"id={self.manifest_id!r}, "
            f"source={self.source.source_id!r}, "
            f"format={self.preferred_format.value}, "
            f"urls={len(self.all_urls)}, "
            f"enabled={self.enabled})"
        )

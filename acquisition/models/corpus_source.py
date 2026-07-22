
from __future__ import annotations

"""
SanskritAI
==========

Corpus Source

Represents a single external acquisition source that can be
downloaded, validated, normalized and imported into the
SanskritAI Knowledge Repository.

A CorpusSource is metadata only.

It does NOT perform downloading or importing.

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

from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_license import SourceLicense
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType


@dataclass(slots=True)
class CorpusSource:
    """
    Represents one external corpus or lexical resource.

    Examples
    --------
    Amarakośa
    Vācaspatyam
    Śabda Kalpadruma
    GRETIL
    SARIT
    Bhagavad Gītā
    Śiva Purāṇa
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    source_id: str
    name: str

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    source_type: SourceType
    source_format: SourceFormat
    license: SourceLicense = SourceLicense.UNKNOWN

    # ------------------------------------------------------------------
    # Versioning
    # ------------------------------------------------------------------

    version: str | None = None
    edition: str | None = None

    # ------------------------------------------------------------------
    # Attribution
    # ------------------------------------------------------------------

    publisher: str | None = None
    author: str | None = None

    description: str | None = None

    language: str = "sa"

    # ------------------------------------------------------------------
    # Acquisition
    # ------------------------------------------------------------------

    status: SourceStatus = SourceStatus.REGISTERED

    download_urls: list[str] = field(default_factory=list)

    checksum: str | None = None

    checksum_algorithm: str = "sha256"

    # ------------------------------------------------------------------
    # Local Storage
    # ------------------------------------------------------------------

    local_path: Path | None = None

    cache_directory: Path | None = None

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    tags: set[str] = field(default_factory=set)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def has_download_url(self) -> bool:
        """Returns True if one or more download URLs exist."""
        return bool(self.download_urls)

    @property
    def is_downloaded(self) -> bool:
        """Returns True if a local copy exists."""
        return self.local_path is not None

    @property
    def is_ready_for_import(self) -> bool:
        """Returns True if acquisition has completed."""
        return self.status.is_importable

    @property
    def filename(self) -> str | None:
        """Returns the filename of the local resource."""
        if self.local_path is None:
            return None

        return self.local_path.name

    # ------------------------------------------------------------------
    # Tag Management
    # ------------------------------------------------------------------

    def add_tag(self, tag: str) -> None:
        """
        Adds a tag to the source.
        """
        tag = tag.strip()

        if tag:
            self.tags.add(tag)

    def remove_tag(self, tag: str) -> None:
        """
        Removes a tag if present.
        """
        self.tags.discard(tag)

    def has_tag(self, tag: str) -> bool:
        """
        Returns True if the source contains the tag.
        """
        return tag in self.tags

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Sets arbitrary metadata.
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
    # URLs
    # ------------------------------------------------------------------

    def add_download_url(self, url: str) -> None:
        """
        Registers a download location.
        """
        url = url.strip()

        if url and url not in self.download_urls:
            self.download_urls.append(url)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def update_status(
        self,
        status: SourceStatus,
    ) -> None:
        """
        Updates acquisition status.
        """
        self.status = status

    # ------------------------------------------------------------------
    # Local Storage
    # ------------------------------------------------------------------

    def set_local_path(
        self,
        path: str | Path,
    ) -> None:
        """
        Records the local acquisition path.
        """
        self.local_path = Path(path)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the source into a JSON-safe dictionary.
        """

        return {
            "source_id": self.source_id,
            "name": self.name,
            "source_type": str(self.source_type),
            "source_format": str(self.source_format),
            "license": str(self.license),
            "version": self.version,
            "edition": self.edition,
            "publisher": self.publisher,
            "author": self.author,
            "description": self.description,
            "language": self.language,
            "status": str(self.status),
            "download_urls": list(self.download_urls),
            "checksum": self.checksum,
            "checksum_algorithm": self.checksum_algorithm,
            "local_path": (
                str(self.local_path)
                if self.local_path
                else None
            ),
            "cache_directory": (
                str(self.cache_directory)
                if self.cache_directory
                else None
            ),
            "tags": sorted(self.tags),
            "metadata": dict(self.metadata),
        }

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"CorpusSource("
            f"id={self.source_id!r}, "
            f"name={self.name!r}, "
            f"type={self.source_type.value}, "
            f"format={self.source_format.value}, "
            f"status={self.status.value})"
        )

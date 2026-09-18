
from __future__ import annotations

"""
SanskritAI
==========

Corpus Source Factory

Creates CorpusSource domain objects from various discovery inputs.

Responsibilities
----------------
* Create CorpusSource from local files
* Create CorpusSource from remote URLs
* Create CorpusSource from metadata
* Populate common metadata consistently

The factory intentionally does NOT:

    • discover resources
    • download files
    • validate files
    • normalize content
    • parse corpora

Version
-------
v0.5.0
"""

from pathlib import Path
from urllib.parse import urlparse

from SanskritAI.acquisition.detectors.source_format_detector import (
    SourceFormatDetector,
)
from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType


class CorpusSourceFactory:
    """
    Factory for constructing CorpusSource objects.
    """

    # ---------------------------------------------------------
    # Local Files
    # ---------------------------------------------------------

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        *,
        source_type: SourceType = SourceType.LOCAL,
        status: SourceStatus = SourceStatus.AVAILABLE,
        metadata: dict | None = None,
    ) -> CorpusSource:

        path = Path(path).expanduser().resolve()

        source_format = SourceFormatDetector.detect(path)

        if source_format is None:
            raise ValueError(
                f"Unsupported source format: {path}"
            )

        file_metadata = dict(metadata or {})

        if path.exists():

            stat = path.stat()

            file_metadata.setdefault(
                "size_bytes",
                stat.st_size,
            )

            file_metadata.setdefault(
                "filename",
                path.name,
            )

            file_metadata.setdefault(
                "directory",
                str(path.parent),
            )

        return CorpusSource(
            identifier=str(path),
            title=path.stem,
            source_type=source_type,
            source_format=source_format,
            status=status,
            local_path=path,
            download_url=None,
            checksum=None,
            description=None,
            license=None,
            metadata=file_metadata,
        )

    # ---------------------------------------------------------
    # Remote URLs
    # ---------------------------------------------------------

    @classmethod
    def from_url(
        cls,
        url: str,
        *,
        title: str | None = None,
        source_type: SourceType = SourceType.REMOTE,
        status: SourceStatus = SourceStatus.AVAILABLE,
        metadata: dict | None = None,
    ) -> CorpusSource:

        parsed = urlparse(url)

        filename = Path(parsed.path).name

        source_format = (
            SourceFormatDetector.detect(filename)
            or SourceFormat.UNKNOWN
        )

        return CorpusSource(
            identifier=url,
            title=title or Path(filename).stem,
            source_type=source_type,
            source_format=source_format,
            status=status,
            local_path=None,
            download_url=url,
            checksum=None,
            description=None,
            license=None,
            metadata=dict(metadata or {}),
        )

    # ---------------------------------------------------------
    # Generic Metadata
    # ---------------------------------------------------------

    @classmethod
    def from_metadata(
        cls,
        *,
        identifier: str,
        title: str,
        source_type: SourceType,
        source_format: SourceFormat,
        status: SourceStatus = SourceStatus.AVAILABLE,
        local_path: str | Path | None = None,
        download_url: str | None = None,
        checksum: str | None = None,
        description: str | None = None,
        license: str | None = None,
        metadata: dict | None = None,
    ) -> CorpusSource:

        if isinstance(local_path, str):
            local_path = Path(local_path)

        return CorpusSource(
            identifier=identifier,
            title=title,
            source_type=source_type,
            source_format=source_format,
            status=status,
            local_path=local_path,
            download_url=download_url,
            checksum=checksum,
            description=description,
            license=license,
            metadata=dict(metadata or {}),
        )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    @staticmethod
    def is_supported(
        path: str | Path,
    ) -> bool:

        return SourceFormatDetector.is_supported(path)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "CorpusSourceFactory()"


from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from urllib.parse import quote

import pytest

from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.corpus_source import (
    CorpusSource,
)

from SanskritAI.acquisition.models.source_format import (
    SourceFormat,
)

from SanskritAI.acquisition.models.source_status import (
    SourceStatus,
)

from SanskritAI.acquisition.models.source_type import (
    SourceType,
)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def make_source(
    identifier: str = "test-source",
) -> CorpusSource:
    return CorpusSource(
        source_id=identifier,
        name="Test Source",
        source_type=SourceType.CORPUS,
        source_format=SourceFormat.TEXT,
    )


def file_url(
    path: Path,
) -> str:
    return path.resolve().as_uri()


def make_manifest(
    *,
    destination: Path,
    urls: list[str] | None = None,
    expected_filename: str | None = "result.txt",
    checksum: str | None = None,
    overwrite_existing: bool = False,
    enabled: bool = True,
) -> AcquisitionManifest:

    return AcquisitionManifest(
        manifest_id="manifest-1",
        source=make_source(),
        urls=list(urls or []),
        expected_filename=expected_filename,
        checksum=checksum,
        destination_directory=destination,
        overwrite_existing=overwrite_existing,
        enabled=enabled,
    )


# ----------------------------------------------------------------------
# Basic
# ----------------------------------------------------------------------

def test_successful_local_file_acquisition(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    source_file.write_text(
        "hello SanskritAI",
        encoding="utf-8",
    )

    destination = tmp_path / "acquired"

    manifest = make_manifest(
        destination=destination,
        urls=[
            file_url(source_file),
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert result.downloaded_file_count == 1
    assert result.downloaded_files[0] == (
        destination / "result.txt"
    )
    assert (
        result.downloaded_files[0].read_text(
            encoding="utf-8",
        )
        == "hello SanskritAI"
    )


def test_result_is_finalized(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    source_file.write_text(
        "content",
        encoding="utf-8",
    )

    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            file_url(source_file),
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.completed_at is not None
    assert result.duration_seconds is not None
    assert result.duration_seconds >= 0


# ----------------------------------------------------------------------
# Destination
# ----------------------------------------------------------------------

def test_existing_destination_file_is_rejected_by_default(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    source_file.write_text(
        "new",
        encoding="utf-8",
    )

    destination = tmp_path / "acquired"
    destination.mkdir()

    target = destination / "result.txt"

    target.write_text(
        "old",
        encoding="utf-8",
    )

    manifest = make_manifest(
        destination=destination,
        urls=[
            file_url(source_file),
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert not result.success
    assert any(
        "already exists" in error
        for error in result.errors
    )


def test_existing_destination_can_be_overwritten(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    source_file.write_text(
        "new",
        encoding="utf-8",
    )

    destination = tmp_path / "acquired"
    destination.mkdir()

    target = destination / "result.txt"

    target.write_text(
        "old",
        encoding="utf-8",
    )

    manifest = make_manifest(
        destination=destination,
        urls=[
            file_url(source_file),
        ],
        overwrite_existing=True,
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert target.read_text(
        encoding="utf-8",
    ) == "new"


# ----------------------------------------------------------------------
# Mirror fallback
# ----------------------------------------------------------------------

def test_failed_primary_url_falls_back_to_mirror(
    tmp_path: Path,
):
    source_file = tmp_path / "mirror.txt"

    source_file.write_text(
        "mirror content",
        encoding="utf-8",
    )

    destination = tmp_path / "acquired"

    manifest = make_manifest(
        destination=destination,
        urls=[
            "file:///does/not/exist.txt",
            file_url(source_file),
        ],
        expected_filename="result.txt",
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success

    assert (
        destination / "result.txt"
    ).read_text(
        encoding="utf-8",
    ) == "mirror content"


# ----------------------------------------------------------------------
# Byte count
# ----------------------------------------------------------------------

def test_bytes_downloaded_are_recorded(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    content = "SanskritAI acquisition"

    source_file.write_text(
        content,
        encoding="utf-8",
    )

    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            file_url(source_file),
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert result.bytes_downloaded == len(
        content.encode("utf-8"),
    )


# ----------------------------------------------------------------------
# Checksum
# ----------------------------------------------------------------------

def test_valid_checksum_is_verified(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    content = b"checksum test"

    source_file.write_bytes(
        content,
    )

    checksum = sha256(
        content,
    ).hexdigest()

    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            file_url(source_file),
        ],
        checksum=checksum,
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert result.checksum_verified


def test_invalid_checksum_fails(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    source_file.write_bytes(
        b"checksum test",
    )

    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            file_url(source_file),
        ],
        checksum="0" * 64,
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert not result.success
    assert not result.checksum_verified
    assert any(
        "Checksum verification failed"
        in error
        for error in result.errors
    )


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

def test_missing_destination_fails():
    manifest = make_manifest(
        destination=None,
        urls=[
            "file:///does/not/exist.txt",
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert not result.success


def test_missing_urls_fails(
    tmp_path: Path,
):
    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert not result.success


def test_disabled_manifest_is_skipped(
    tmp_path: Path,
):
    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[],
        enabled=False,
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert manifest.source.status == (
        SourceStatus.SKIPPED
    )
    assert (
        result.message
        == "Acquisition manifest is disabled."
    )


# ----------------------------------------------------------------------
# Source lifecycle
# ----------------------------------------------------------------------

def test_successful_acquisition_updates_source_status(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    source_file.write_text(
        "content",
        encoding="utf-8",
    )

    destination = tmp_path / "acquired"

    manifest = make_manifest(
        destination=destination,
        urls=[
            file_url(source_file),
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert manifest.source.status == (
        SourceStatus.DOWNLOADED
    )


def test_successful_checksum_acquisition_reaches_validated(
    tmp_path: Path,
):
    source_file = tmp_path / "source.txt"

    content = b"validated content"

    source_file.write_bytes(
        content,
    )

    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            file_url(source_file),
        ],
        checksum=sha256(
            content,
        ).hexdigest(),
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert manifest.source.status == (
        SourceStatus.VALIDATED
    )


def test_failed_acquisition_updates_source_status(
    tmp_path: Path,
):
    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            "file:///does/not/exist.txt",
        ],
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert not result.success
    assert manifest.source.status == (
        SourceStatus.FAILED
    )


# ----------------------------------------------------------------------
# Source identity
# ----------------------------------------------------------------------

def test_result_preserves_source_identity(
    tmp_path: Path,
):
    source = make_source(
        "amarakosha",
    )

    source_file = tmp_path / "source.txt"

    source_file.write_text(
        "amarakosha",
        encoding="utf-8",
    )

    manifest = AcquisitionManifest(
        manifest_id="manifest-amarakosha",
        source=source,
        urls=[
            file_url(source_file),
        ],
        expected_filename="amarakosha.txt",
        destination_directory=(
            tmp_path / "acquired"
        ),
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.source is source
    assert result.source.source_id == (
        "amarakosha"
    )


# ----------------------------------------------------------------------
# Filename resolution
# ----------------------------------------------------------------------

def test_url_filename_is_used_when_expected_filename_missing(
    tmp_path: Path,
):
    source_file = tmp_path / "actual.txt"

    source_file.write_text(
        "content",
        encoding="utf-8",
    )

    manifest = make_manifest(
        destination=tmp_path / "acquired",
        urls=[
            file_url(source_file),
        ],
        expected_filename=None,
    )

    result = DefaultSourceAcquirer().acquire(
        manifest,
    )

    assert result.success
    assert (
        tmp_path
        / "acquired"
        / "actual.txt"
    ).exists()

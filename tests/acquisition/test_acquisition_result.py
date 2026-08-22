
from pathlib import Path

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)
from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_type import SourceType


def make_source() -> CorpusSource:
    return CorpusSource(
        source_id="test-source",
        name="Test Source",
        source_type=SourceType.CORPUS,
        source_format=SourceFormat.TXT,
    )


def test_result_construction():
    result = AcquisitionResult(
        source=make_source(),
    )

    assert result.source.source_id == "test-source"
    assert result.success
    assert result.message == ""
    assert result.completed_at is None
    assert result.duration_seconds is None


def test_finalize_sets_completion_information():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.finalize()

    assert result.completed_at is not None
    assert result.duration_seconds is not None
    assert result.duration_seconds >= 0


def test_warning_management():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.add_warning(" warning ")

    assert result.has_warnings
    assert result.warnings == ["warning"]
    assert result.success


def test_empty_warning_is_ignored():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.add_warning("   ")

    assert not result.has_warnings


def test_error_marks_result_failed():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.add_error(" checksum failed ")

    assert result.has_errors
    assert result.errors == ["checksum failed"]
    assert not result.success


def test_empty_error_is_ignored():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.add_error("   ")

    assert not result.has_errors
    assert result.success


def test_downloaded_files():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.add_downloaded_file("/tmp/source.txt")
    result.add_downloaded_file(
        Path("/tmp/source.xml")
    )

    assert result.downloaded_file_count == 2
    assert result.downloaded_files == [
        Path("/tmp/source.txt"),
        Path("/tmp/source.xml"),
    ]


def test_extracted_files():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.add_extracted_file("/tmp/page1.txt")
    result.add_extracted_file("/tmp/page2.txt")

    assert result.extracted_file_count == 2
    assert result.extracted_files == [
        Path("/tmp/page1.txt"),
        Path("/tmp/page2.txt"),
    ]


def test_metadata():
    result = AcquisitionResult(
        source=make_source(),
    )

    result.set_metadata("provider", "test")

    assert result.get_metadata("provider") == "test"
    assert result.get_metadata("missing") is None
    assert result.get_metadata("missing", "fallback") == "fallback"


def test_to_dict():
    result = AcquisitionResult(
        source=make_source(),
        message="Acquisition completed",
    )

    result.add_downloaded_file("/tmp/source.txt")
    result.add_extracted_file("/tmp/page.txt")
    result.add_warning("minor warning")
    result.set_metadata("provider", "test")

    result.bytes_downloaded = 1024
    result.checksum_verified = True
    result.license_verified = True
    result.normalized = True
    result.imported = True

    result.finalize()

    data = result.to_dict()

    assert data["source_id"] == "test-source"
    assert data["success"] is True
    assert data["message"] == "Acquisition completed"
    assert data["downloaded_files"] == ["/tmp/source.txt"]
    assert data["extracted_files"] == ["/tmp/page.txt"]
    assert data["bytes_downloaded"] == 1024
    assert data["checksum_verified"] is True
    assert data["license_verified"] is True
    assert data["normalized"] is True
    assert data["imported"] is True
    assert data["warnings"] == ["minor warning"]
    assert data["errors"] == []
    assert data["metadata"]["provider"] == "test"


def test_repr_contains_identity():
    result = AcquisitionResult(
        source=make_source(),
    )

    text = repr(result)

    assert "test-source" in text
    assert "success=True" in text


from pathlib import Path

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)
from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_license import SourceLicense
from SanskritAI.acquisition.models.source_type import SourceType


def make_source() -> CorpusSource:
    return CorpusSource(
        source_id="gretl-gita",
        name="Bhagavad Gītā",
        source_type=SourceType.CORPUS,
        source_format=SourceFormat.TXT,
        license=SourceLicense.UNKNOWN,
    )


def make_manifest() -> AcquisitionManifest:
    return AcquisitionManifest(
        manifest_id="gretl-gita-txt",
        source=make_source(),
        preferred_format=SourceFormat.TXT,
    )


def test_manifest_construction():
    manifest = make_manifest()

    assert manifest.manifest_id == "gretl-gita-txt"
    assert manifest.source.source_id == "gretl-gita"
    assert manifest.preferred_format is SourceFormat.TXT
    assert manifest.enabled
    assert manifest.priority == 100


def test_url_management():
    manifest = make_manifest()

    manifest.add_url(" https://example.org/gita.txt ")
    manifest.add_mirror(" https://mirror.example.org/gita.txt ")

    assert manifest.urls == [
        "https://example.org/gita.txt"
    ]
    assert manifest.mirrors == [
        "https://mirror.example.org/gita.txt"
    ]

    assert manifest.all_urls == [
        "https://example.org/gita.txt",
        "https://mirror.example.org/gita.txt",
    ]


def test_duplicate_urls_are_ignored():
    manifest = make_manifest()

    manifest.add_url("https://example.org/gita.txt")
    manifest.add_url("https://example.org/gita.txt")

    manifest.add_mirror("https://mirror.example.org/gita.txt")
    manifest.add_mirror("https://mirror.example.org/gita.txt")

    assert len(manifest.urls) == 1
    assert len(manifest.mirrors) == 1


def test_empty_urls_are_ignored():
    manifest = make_manifest()

    manifest.add_url("   ")
    manifest.add_mirror("   ")

    assert manifest.urls == []
    assert manifest.mirrors == []


def test_download_requirement():
    manifest = make_manifest()

    assert not manifest.requires_download

    manifest.add_url("https://example.org/gita.txt")

    assert manifest.has_urls
    assert manifest.requires_download


def test_checksum_requirement():
    manifest = make_manifest()

    assert not manifest.requires_checksum_validation

    manifest.checksum = "abc123"

    assert manifest.requires_checksum_validation

    manifest.validate_checksum = False

    assert not manifest.requires_checksum_validation


def test_license_validation_requirement():
    manifest = make_manifest()

    assert manifest.requires_license_validation

    manifest.validate_license = False

    assert not manifest.requires_license_validation


def test_metadata():
    manifest = make_manifest()

    manifest.set_metadata("provider", "GRETIL")

    assert manifest.get_metadata("provider") == "GRETIL"
    assert manifest.get_metadata("missing") is None
    assert manifest.get_metadata("missing", "fallback") == "fallback"


def test_to_dict():
    manifest = make_manifest()

    manifest.add_url("https://example.org/gita.txt")
    manifest.add_mirror("https://mirror.example.org/gita.txt")
    manifest.destination_directory = Path("/tmp/data")
    manifest.cache_directory = Path("/tmp/cache")
    manifest.set_metadata("provider", "GRETIL")

    data = manifest.to_dict()

    assert data["manifest_id"] == "gretl-gita-txt"
    assert data["source_id"] == "gretl-gita"
    assert data["urls"] == [
        "https://example.org/gita.txt"
    ]
    assert data["mirrors"] == [
        "https://mirror.example.org/gita.txt"
    ]
    assert data["preferred_format"] == "txt"
    assert data["destination_directory"] == "/tmp/data"
    assert data["cache_directory"] == "/tmp/cache"
    assert data["metadata"]["provider"] == "GRETIL"


def test_repr_contains_identity():
    manifest = make_manifest()

    text = repr(manifest)

    assert "gretl-gita-txt" in text
    assert "gretl-gita" in text
    assert "txt" in text


from pathlib import Path

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_license import SourceLicense
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType


def make_source() -> CorpusSource:
    return CorpusSource(
        source_id="amarakosha",
        name="Amarakośa",
        source_type=SourceType.LEXICON,
        source_format=SourceFormat.XML,
        license=SourceLicense.PUBLIC_DOMAIN,
    )


def test_corpus_source_construction():
    source = make_source()

    assert source.source_id == "amarakosha"
    assert source.name == "Amarakośa"
    assert source.source_type is SourceType.LEXICON
    assert source.source_format is SourceFormat.XML
    assert source.license is SourceLicense.PUBLIC_DOMAIN


def test_default_state():
    source = make_source()

    assert source.status is SourceStatus.REGISTERED
    assert not source.has_download_url
    assert not source.is_downloaded
    assert not source.is_ready_for_import


def test_download_url_management():
    source = make_source()

    source.add_download_url(" https://example.org/a.xml ")

    assert source.has_download_url
    assert source.download_urls == [
        "https://example.org/a.xml"
    ]


def test_duplicate_download_urls_are_ignored():
    source = make_source()

    source.add_download_url("https://example.org/a.xml")
    source.add_download_url("https://example.org/a.xml")

    assert source.download_urls == [
        "https://example.org/a.xml"
    ]


def test_tag_management():
    source = make_source()

    source.add_tag("lexicon")
    source.add_tag("  Sanskrit  ")

    assert source.has_tag("lexicon")
    assert source.has_tag("Sanskrit")

    source.remove_tag("lexicon")

    assert not source.has_tag("lexicon")


def test_empty_tag_is_ignored():
    source = make_source()

    source.add_tag("   ")

    assert not source.tags


def test_metadata_management():
    source = make_source()

    source.set_metadata("publisher", "Test Publisher")

    assert source.get_metadata("publisher") == "Test Publisher"
    assert source.get_metadata("missing") is None
    assert source.get_metadata("missing", "default") == "default"


def test_local_path_and_filename():
    source = make_source()

    source.set_local_path("/tmp/amarakosha.xml")

    assert source.local_path == Path("/tmp/amarakosha.xml")
    assert source.filename == "amarakosha.xml"
    assert source.is_downloaded


def test_status_and_importability():
    source = make_source()

    source.update_status(SourceStatus.READY_FOR_IMPORT)

    assert source.status is SourceStatus.READY_FOR_IMPORT
    assert source.is_ready_for_import


def test_to_dict():
    source = make_source()

    source.add_download_url("https://example.org/a.xml")
    source.add_tag("lexicon")
    source.set_local_path("/tmp/a.xml")
    source.set_metadata("edition", "test")

    data = source.to_dict()

    assert data["source_id"] == "amarakosha"
    assert data["name"] == "Amarakośa"
    assert data["source_type"] == "lexicon"
    assert data["source_format"] == "xml"
    assert data["license"] == "public_domain"
    assert data["download_urls"] == [
        "https://example.org/a.xml"
    ]
    assert data["local_path"] == "/tmp/a.xml"
    assert data["tags"] == ["lexicon"]
    assert data["metadata"]["edition"] == "test"


def test_repr_contains_identity():
    source = make_source()

    text = repr(source)

    assert "amarakosha" in text
    assert "Amarakośa" in text
    assert "lexicon" in text
    assert "xml" in text


from __future__ import annotations

from dataclasses import FrozenInstanceError
from dataclasses import dataclass
from pathlib import Path

import pytest

from SanskritAI.acquisition.knowledge.abstract_lexical_manifest import (
    AbstractLexicalManifest,
)


# ---------------------------------------------------------------------------
# Concrete test implementation
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class _ConcreteManifest(AbstractLexicalManifest):
    """
    Minimal concrete implementation used exclusively for testing
    AbstractLexicalManifest.

    The class is deliberately slotted and frozen so that the test
    implementation preserves the structural contract of the abstract
    manifest.
    """

    @property
    def identifier(self) -> str:
        return self.short_name

    def summary(self) -> dict:
        return {
            "identifier": self.identifier,
            "resource_name": self.resource_name,
            "short_name": self.short_name,
            "version": self.version,
            "provider": self.provider,
            "language": self.language,
            "script": self.script,
        }


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_manifest(
    *,
    resource_name: str = "Test Dictionary",
    short_name: str = "TEST",
    version: str = "1.0",
    provider: str = "Test Provider",
    source_url: str | None = None,
    download_url: str | None = None,
    homepage: str | None = None,
    language: str = "sa",
    script: str = "Devanagari",
    transliteration_scheme: str | None = None,
    local_directory: Path | None = None,
    source_filename: str | None = None,
    encoding: str = "utf-8",
    checksum: str | None = None,
    edition: str | None = None,
    publication_year: int | None = None,
    license_name: str | None = None,
    attribution: str | None = None,
    copyright_notice: str | None = None,
    metadata: dict | None = None,
) -> _ConcreteManifest:

    return _ConcreteManifest(
        resource_name=resource_name,
        short_name=short_name,
        version=version,
        provider=provider,
        source_url=source_url,
        download_url=download_url,
        homepage=homepage,
        language=language,
        script=script,
        transliteration_scheme=transliteration_scheme,
        local_directory=local_directory,
        source_filename=source_filename,
        encoding=encoding,
        checksum=checksum,
        edition=edition,
        publication_year=publication_year,
        license_name=license_name,
        attribution=attribution,
        copyright_notice=copyright_notice,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Abstract contract
# ---------------------------------------------------------------------------

def test_manifest_is_abstract():
    """
    AbstractLexicalManifest must not be directly instantiable because
    identifier and summary are abstract behaviours.
    """

    with pytest.raises(TypeError):
        AbstractLexicalManifest(
            resource_name="Test",
            short_name="TEST",
            version="1.0",
            provider="Provider",
        )


def test_concrete_manifest_is_instantiable():
    manifest = make_manifest()

    assert isinstance(
        manifest,
        AbstractLexicalManifest,
    )


def test_identifier_is_required_contract():
    manifest = make_manifest(
        short_name="MW",
    )

    assert manifest.identifier == "MW"


def test_summary_is_required_contract():
    manifest = make_manifest(
        short_name="MW",
        resource_name="Monier-Williams",
    )

    summary = manifest.summary()

    assert isinstance(summary, dict)
    assert summary["identifier"] == "MW"
    assert summary["resource_name"] == "Monier-Williams"


# ---------------------------------------------------------------------------
# Identity metadata
# ---------------------------------------------------------------------------

def test_identity_fields_are_preserved():
    manifest = make_manifest(
        resource_name="Monier-Williams Sanskrit-English Dictionary",
        short_name="MW",
        version="1.0",
        provider="Test Provider",
    )

    assert (
        manifest.resource_name
        == "Monier-Williams Sanskrit-English Dictionary"
    )
    assert manifest.short_name == "MW"
    assert manifest.version == "1.0"
    assert manifest.provider == "Test Provider"


# ---------------------------------------------------------------------------
# Default values
# ---------------------------------------------------------------------------

def test_default_language_is_sanskrit():
    manifest = make_manifest()

    assert manifest.language == "sa"


def test_default_script_is_devanagari():
    manifest = make_manifest()

    assert manifest.script == "Devanagari"


def test_default_encoding_is_utf8():
    manifest = make_manifest()

    assert manifest.encoding == "utf-8"


def test_optional_source_fields_default_to_none():
    manifest = make_manifest()

    assert manifest.source_url is None
    assert manifest.download_url is None
    assert manifest.homepage is None


def test_optional_local_acquisition_fields_default_to_none():
    manifest = make_manifest()

    assert manifest.local_directory is None
    assert manifest.source_filename is None
    assert manifest.checksum is None


def test_optional_publication_fields_default_to_none():
    manifest = make_manifest()

    assert manifest.edition is None
    assert manifest.publication_year is None
    assert manifest.license_name is None
    assert manifest.attribution is None
    assert manifest.copyright_notice is None


def test_optional_metadata_defaults_to_none():
    manifest = make_manifest()

    assert manifest.metadata is None


# ---------------------------------------------------------------------------
# Convenience properties
# ---------------------------------------------------------------------------

def test_display_name_defaults_to_resource_name():
    manifest = make_manifest(
        resource_name="Amarakosha",
    )

    assert manifest.display_name == "Amarakosha"


def test_has_download_is_false_without_download_url():
    manifest = make_manifest()

    assert manifest.has_download is False


def test_has_download_is_true_with_download_url():
    manifest = make_manifest(
        download_url="https://example.org/test.zip",
    )

    assert manifest.has_download is True


def test_has_local_copy_is_false_without_local_directory():
    manifest = make_manifest()

    assert manifest.has_local_copy is False


def test_has_local_copy_is_true_with_local_directory():
    manifest = make_manifest(
        local_directory=Path("/tmp/test-dictionary"),
    )

    assert manifest.has_local_copy is True


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------

def test_manifest_is_frozen():
    manifest = make_manifest()

    with pytest.raises(FrozenInstanceError):
        manifest.version = "2.0"


# ---------------------------------------------------------------------------
# Slots
# ---------------------------------------------------------------------------

def test_manifest_is_slot_based():
    """
    The concrete test implementation must preserve the slots contract.

    The abstract base is declared with:
        @dataclass(frozen=True, slots=True)

    Therefore the concrete test implementation is also declared with
    slots=True. This avoids introducing a __dict__ through the test
    subclass itself.
    """

    manifest = make_manifest()

    assert not hasattr(
        manifest,
        "__dict__",
    )


def test_manifest_has_no_instance_dictionary():
    manifest = make_manifest()

    assert "__dict__" not in dir(manifest)


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------

def test_string_representation_contains_class_name():
    manifest = make_manifest(
        short_name="MW",
        version="1.0",
    )

    value = str(manifest)

    assert "_ConcreteManifest" in value


def test_string_representation_contains_identifier():
    manifest = make_manifest(
        short_name="MW",
    )

    assert "identifier='MW'" in str(manifest)


def test_string_representation_contains_version():
    manifest = make_manifest(
        version="2.5",
    )

    assert "version='2.5'" in str(manifest)


# ---------------------------------------------------------------------------
# Rich metadata
# ---------------------------------------------------------------------------

def test_manifest_accepts_complete_metadata():
    metadata = {
        "source_type": "dictionary",
        "edition": "critical",
        "language_family": "Indo-European",
    }

    manifest = make_manifest(
        source_url="https://example.org/source",
        download_url="https://example.org/download",
        homepage="https://example.org",
        transliteration_scheme="IAST",
        local_directory=Path("/tmp/test"),
        source_filename="dictionary.txt",
        checksum="abc123",
        edition="First Edition",
        publication_year=1899,
        license_name="Public Domain",
        attribution="Test Attribution",
        copyright_notice="Test Notice",
        metadata=metadata,
    )

    assert manifest.source_url == "https://example.org/source"
    assert manifest.download_url == "https://example.org/download"
    assert manifest.homepage == "https://example.org"
    assert manifest.transliteration_scheme == "IAST"
    assert manifest.local_directory == Path("/tmp/test")
    assert manifest.source_filename == "dictionary.txt"
    assert manifest.checksum == "abc123"
    assert manifest.edition == "First Edition"
    assert manifest.publication_year == 1899
    assert manifest.license_name == "Public Domain"
    assert manifest.attribution == "Test Attribution"
    assert manifest.copyright_notice == "Test Notice"
    assert manifest.metadata == metadata

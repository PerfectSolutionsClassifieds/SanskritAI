
from pathlib import Path

import pytest

from SanskritAI.acquisition.knowledge.abstract_lexical_manifest import (
    AbstractLexicalManifest,
)


# ---------------------------------------------------------------------------
# Test implementation
# ---------------------------------------------------------------------------


class TestManifest(AbstractLexicalManifest):
    """
    Minimal concrete implementation used only to exercise the abstract
    manifest contract.
    """

    @property
    def identifier(self) -> str:
        return self.short_name

    def summary(self) -> dict:
        return {
            "identifier": self.identifier,
            "resource": self.resource_name,
            "version": self.version,
        }


def make_manifest(**overrides):
    values = {
        "resource_name": "Test Dictionary",
        "short_name": "TEST",
        "version": "1.0",
        "provider": "Test Provider",
    }

    values.update(overrides)

    return TestManifest(**values)


# ---------------------------------------------------------------------------
# Abstract contract
# ---------------------------------------------------------------------------


def test_abstract_manifest_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractLexicalManifest(
            resource_name="Test",
            short_name="TEST",
            version="1.0",
            provider="Provider",
        )


def test_concrete_manifest_can_be_instantiated():
    manifest = make_manifest()

    assert isinstance(manifest, AbstractLexicalManifest)


# ---------------------------------------------------------------------------
# Required metadata
# ---------------------------------------------------------------------------


def test_required_identity_metadata_is_preserved():
    manifest = make_manifest(
        resource_name="Monier-Williams",
        short_name="MW",
        version="1899",
        provider="Oxford",
    )

    assert manifest.resource_name == "Monier-Williams"
    assert manifest.short_name == "MW"
    assert manifest.version == "1899"
    assert manifest.provider == "Oxford"


def test_default_resource_characteristics_are_applied():
    manifest = make_manifest()

    assert manifest.language == "sa"
    assert manifest.script == "Devanagari"
    assert manifest.encoding == "utf-8"


def test_optional_source_metadata_defaults_to_none():
    manifest = make_manifest()

    assert manifest.source_url is None
    assert manifest.download_url is None
    assert manifest.homepage is None
    assert manifest.transliteration_scheme is None
    assert manifest.local_directory is None
    assert manifest.source_filename is None
    assert manifest.checksum is None
    assert manifest.edition is None
    assert manifest.publication_year is None
    assert manifest.license_name is None
    assert manifest.attribution is None
    assert manifest.copyright_notice is None
    assert manifest.metadata is None


# ---------------------------------------------------------------------------
# Identifier
# ---------------------------------------------------------------------------


def test_identifier_is_supplied_by_concrete_manifest():
    manifest = make_manifest(
        short_name="MW",
    )

    assert manifest.identifier == "MW"


# ---------------------------------------------------------------------------
# Convenience properties
# ---------------------------------------------------------------------------


def test_display_name_defaults_to_resource_name():
    manifest = make_manifest(
        resource_name="Monier-Williams Sanskrit-English Dictionary",
    )

    assert manifest.display_name == manifest.resource_name


def test_has_download_is_false_when_download_url_is_missing():
    manifest = make_manifest(
        download_url=None,
    )

    assert manifest.has_download is False


def test_has_download_is_true_when_download_url_exists():
    manifest = make_manifest(
        download_url="https://example.org/test.zip",
    )

    assert manifest.has_download is True


def test_has_local_copy_is_false_when_local_directory_is_missing():
    manifest = make_manifest(
        local_directory=None,
    )

    assert manifest.has_local_copy is False


def test_has_local_copy_is_true_when_local_directory_exists():
    manifest = make_manifest(
        local_directory=Path("/tmp/test-dictionary"),
    )

    assert manifest.has_local_copy is True


# ---------------------------------------------------------------------------
# Additional metadata
# ---------------------------------------------------------------------------


def test_optional_metadata_is_preserved():
    metadata = {
        "format": "xml",
        "entries": 100,
    }

    manifest = make_manifest(
        language="sa",
        script="Devanagari",
        transliteration_scheme="IAST",
        local_directory=Path("/tmp/mw"),
        source_filename="mw.xml",
        checksum="abc123",
        edition="First Edition",
        publication_year=1899,
        license_name="Test License",
        attribution="Test Attribution",
        copyright_notice="Test Notice",
        metadata=metadata,
    )

    assert manifest.language == "sa"
    assert manifest.script == "Devanagari"
    assert manifest.transliteration_scheme == "IAST"
    assert manifest.local_directory == Path("/tmp/mw")
    assert manifest.source_filename == "mw.xml"
    assert manifest.checksum == "abc123"
    assert manifest.edition == "First Edition"
    assert manifest.publication_year == 1899
    assert manifest.license_name == "Test License"
    assert manifest.attribution == "Test Attribution"
    assert manifest.copyright_notice == "Test Notice"
    assert manifest.metadata == metadata


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


def test_manifest_is_frozen():
    manifest = make_manifest()

    with pytest.raises(AttributeError):
        manifest.resource_name = "Changed"


def test_manifest_is_slot_based():
    manifest = make_manifest()

    assert not hasattr(manifest, "__dict__")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def test_summary_is_defined_by_concrete_manifest():
    manifest = make_manifest(
        short_name="TEST",
        version="2.0",
    )

    summary = manifest.summary()

    assert isinstance(summary, dict)
    assert summary["identifier"] == "TEST"
    assert summary["resource"] == "Test Dictionary"
    assert summary["version"] == "2.0"


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------


def test_string_representation_contains_class_identifier_and_version():
    manifest = make_manifest(
        short_name="MW",
        version="1899",
    )

    value = str(manifest)

    assert value == (
        "TestManifest(identifier='MW', version='1899')"
    )

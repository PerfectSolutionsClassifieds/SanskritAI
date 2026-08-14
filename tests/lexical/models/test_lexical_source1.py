import pytest

from SanskritAI.lexical.models.lexical_source import LexicalSource
from SanskritAI.lexical.models.lexical_source_metadata import LexicalSourceMetadata

def test_lexical_source_stores_identifier_and_name():
    source = LexicalSource(
        identifier="monier-williams",
        name="Monier-Williams Sanskrit-English Dictionary",
    )
    assert source.identifier == "monier-williams"
    assert source.name == "Monier-Williams Sanskrit-English Dictionary"

def test_lexical_source_metadata_is_optional():
    source = LexicalSource(
        identifier="apte",
        name="Apte Sanskrit-English Dictionary",
    )
    assert source.metadata is None

def test_lexical_source_accepts_metadata():
    metadata = LexicalSourceMetadata(
        description="Sanskrit-English lexical dictionary.",
        language="Sanskrit",
        script="Devanagari",
        edition="Revised Edition",
        publisher="Test Publisher",
        year=2026,
    )
    source = LexicalSource(
        identifier="apte",
        name="Apte Sanskrit-English Dictionary",
        metadata=metadata,
    )
    assert source.metadata is metadata
    assert source.metadata.language == "Sanskrit"

def test_lexical_source_rejects_empty_identifier():
    with pytest.raises(ValueError, match="identifier"):
        LexicalSource(
            identifier="",
            name="Test Source",
        )

def test_lexical_source_rejects_empty_name():
    with pytest.raises(ValueError, match="name"):
        LexicalSource(
            identifier="test-source",
            name="",
        )

def test_lexical_source_is_immutable():
    source = LexicalSource(
        identifier="amara",
        name="Amarakośa",
    )
    with pytest.raises(AttributeError):
        source.name = "Changed"

def test_lexical_source_string_representation():
    source = LexicalSource(
        identifier="amara",
        name="Amarakośa",
    )
    assert str(source) == "Amarakośa"

import pytest

from SanskritAI.lexical.models.base_lexical_metadata import BaseLexicalMetadata
from SanskritAI.lexical.models.lexical_record import LexicalRecord
from SanskritAI.lexical.models.lexical_source import LexicalSource

class ConcreteLexicalRecord(LexicalRecord):
    pass

@pytest.fixture
def source():
    return LexicalSource(
        identifier="monier-williams",
        name="Monier-Williams Sanskrit-English Dictionary",
    )

@pytest.fixture
def metadata():
    return BaseLexicalMetadata()

@pytest.fixture
def record(source, metadata):
    return ConcreteLexicalRecord(
        identifier="mw-000001",
        metadata=metadata,
        source=source,
    )

def test_lexical_record_is_constructed(record):
    assert record.identifier == "mw-000001"

def test_lexical_record_exposes_source(record, source):
    assert record.source is source

def test_lexical_record_exposes_source_name(record):
    assert (
        record.source_name
        == "Monier-Williams Sanskrit-English Dictionary"
    )

def test_lexical_record_exposes_source_identifier(record):
    assert record.source_identifier == "monier-williams"

def test_lexical_record_preserves_metadata(record, metadata):
    assert record.metadata is metadata

def test_lexical_record_requires_source(metadata):
    with pytest.raises(TypeError):
        ConcreteLexicalRecord(
            identifier="mw-000002",
            metadata=metadata,
        )

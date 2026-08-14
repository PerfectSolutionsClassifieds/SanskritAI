
from SanskritAI.corpus.models.document_metadata import DocumentMetadata


def test_default_construction():
    metadata = DocumentMetadata()

    assert metadata is not None


def test_to_dict_returns_dict():
    metadata = DocumentMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_metadata_fields():
    metadata = DocumentMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_repr_is_available():
    metadata = DocumentMetadata()

    assert "DocumentMetadata" in repr(metadata)

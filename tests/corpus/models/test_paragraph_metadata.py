
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata


def test_default_construction():
    metadata = ParagraphMetadata()

    assert metadata is not None


def test_to_dict_returns_dict():
    metadata = ParagraphMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_metadata_fields():
    metadata = ParagraphMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_repr_is_available():
    metadata = ParagraphMetadata()

    assert "ParagraphMetadata" in repr(metadata)

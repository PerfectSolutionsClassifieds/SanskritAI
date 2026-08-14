
from SanskritAI.corpus.models.verse_metadata import VerseMetadata


def test_default_construction():
    metadata = VerseMetadata()

    assert metadata is not None


def test_to_dict_returns_dict():
    metadata = VerseMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_metadata_fields():
    metadata = VerseMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_repr_is_available():
    metadata = VerseMetadata()

    assert "VerseMetadata" in repr(metadata)

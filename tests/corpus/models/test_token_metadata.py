
from SanskritAI.corpus.models.token_metadata import TokenMetadata


def test_default_construction():
    metadata = TokenMetadata()

    assert metadata is not None


def test_to_dict_returns_dict():
    metadata = TokenMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_metadata_fields():
    metadata = TokenMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_repr_is_available():
    metadata = TokenMetadata()

    assert "TokenMetadata" in repr(metadata)

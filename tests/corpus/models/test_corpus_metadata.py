
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata


def test_default_construction():
    metadata = CorpusMetadata()

    assert metadata is not None


def test_to_dict_returns_dict():
    metadata = CorpusMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_metadata_fields():
    metadata = CorpusMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_repr_is_available():
    metadata = CorpusMetadata()

    assert "CorpusMetadata" in repr(metadata)

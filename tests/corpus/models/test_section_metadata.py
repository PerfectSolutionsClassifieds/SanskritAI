
from SanskritAI.corpus.models.section_metadata import SectionMetadata


def test_default_construction():
    metadata = SectionMetadata()

    assert metadata is not None


def test_to_dict_returns_dict():
    metadata = SectionMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_metadata_fields():
    metadata = SectionMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_repr_is_available():
    metadata = SectionMetadata()

    assert "SectionMetadata" in repr(metadata)

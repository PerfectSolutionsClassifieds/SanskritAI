
from SanskritAI.corpus.models.line_metadata import LineMetadata


def test_default_construction():
    metadata = LineMetadata()

    assert metadata is not None


def test_default_language_is_sanskrit():
    metadata = LineMetadata()

    assert metadata.language == "sanskrit"


def test_language_can_be_specified():
    metadata = LineMetadata(language="sanskrit")

    assert metadata.language == "sanskrit"


def test_to_dict_returns_dict():
    metadata = LineMetadata()

    result = metadata.to_dict()

    assert isinstance(result, dict)


def test_to_dict_contains_language():
    metadata = LineMetadata(language="sanskrit")

    result = metadata.to_dict()

    assert result["language"] == "sanskrit"


def test_repr_is_available():
    metadata = LineMetadata()

    assert "LineMetadata" in repr(metadata)

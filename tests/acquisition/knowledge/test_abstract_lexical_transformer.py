import pytest

from SanskritAI.acquisition.knowledge.abstract_lexical_transformer import (
    AbstractLexicalTransformer,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)
from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


# ---------------------------------------------------------------------------
# Test implementation
# ---------------------------------------------------------------------------


class DummyTransformer(AbstractLexicalTransformer):
    """Minimal concrete transformer used to exercise the abstract transformer contract and its batch/diagnostic helpers."""

    def __init__(
        self,
        resource_name: str = "Test Dictionary",
        resource_version: str = "unknown",
    ) -> None:
        super().__init__(
            resource_name=resource_name,
            resource_version=resource_version,
        )

    def transform(
        self,
        entry: RawLexicalEntry,
    ) -> CanonicalLexicalRecord:
        return CanonicalLexicalRecord(
            headword=entry.headword,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_transformer(**overrides):
    values = {
        "resource_name": "Test Dictionary",
    }
    values.update(overrides)
    return DummyTransformer(**values)


def make_entry(
    headword: str = "राम",
):
    return RawLexicalEntry(
        headword=headword,
        source_name="Test Source",
        source_version="1.0",
        source_record_id="1",
    )


# ---------------------------------------------------------------------------
# Abstract contract
# ---------------------------------------------------------------------------


def test_abstract_transformer_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractLexicalTransformer(
            resource_name="Test Dictionary",
        )


def test_concrete_transformer_can_be_instantiated():
    transformer = make_transformer()
    assert isinstance(
        transformer,
        AbstractLexicalTransformer,
    )


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


def test_resource_name_is_preserved():
    transformer = make_transformer(
        resource_name="Monier-Williams",
    )
    assert transformer.resource_name == "Monier-Williams"


def test_default_resource_version_is_unknown():
    transformer = make_transformer()
    assert transformer.resource_version == "unknown"


def test_custom_resource_version_is_preserved():
    transformer = make_transformer(
        resource_version="1899",
    )
    assert transformer.resource_version == "1899"


# ---------------------------------------------------------------------------
# Identifier
# ---------------------------------------------------------------------------


def test_identifier_defaults_to_concrete_class_name():
    transformer = make_transformer()
    assert transformer.identifier == "DummyTransformer"


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------


def test_transform_returns_canonical_lexical_record():
    transformer = make_transformer()
    entry = make_entry("राम")
    result = transformer.transform(entry)
    assert isinstance(
        result,
        CanonicalLexicalRecord,
    )
    assert result.headword == "राम"


def test_transform_preserves_headword_for_multiple_entries():
    transformer = make_transformer()
    first = transformer.transform(
        make_entry("राम"),
    )
    second = transformer.transform(
        make_entry("हरि"),
    )
    assert first.headword == "राम"
    assert second.headword == "हरि"


# ---------------------------------------------------------------------------
# Batch transformation
# ---------------------------------------------------------------------------


def test_transform_all_returns_tuple():
    transformer = make_transformer()
    entries = [
        make_entry("राम"),
        make_entry("हरि"),
        make_entry("कृष्ण"),
    ]
    result = transformer.transform_all(entries)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert all(
        isinstance(
            record,
            CanonicalLexicalRecord,
        )
        for record in result
    )


def test_transform_all_preserves_input_order():
    transformer = make_transformer()
    entries = (
        make_entry("राम"),
        make_entry("हरि"),
        make_entry("कृष्ण"),
    )
    result = transformer.transform_all(entries)
    assert tuple(record.headword for record in result) == (
        "राम",
        "हरि",
        "कृष्ण",
    )


def test_transform_all_accepts_generators():
    transformer = make_transformer()
    entries = (
        make_entry(word)
        for word in (
            "राम",
            "हरि",
            "कृष्ण",
        )
    )
    result = transformer.transform_all(entries)
    assert tuple(record.headword for record in result) == (
        "राम",
        "हरि",
        "कृष्ण",
    )


def test_transform_all_empty_input_returns_empty_tuple():
    transformer = make_transformer()
    assert transformer.transform_all([]) == ()


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


def test_summary_contains_transformer_diagnostics():
    transformer = make_transformer(
        resource_name="Monier-Williams",
        resource_version="1899",
    )
    assert transformer.summary() == {
        "transformer": "DummyTransformer",
        "resource": "Monier-Williams",
        "version": "1899",
        "target": "CanonicalLexicalRecord",
    }


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------


def test_string_representation_contains_class_and_resource():
    transformer = make_transformer(
        resource_name="Monier-Williams",
    )
    assert str(transformer) == (
        "DummyTransformer(resource='Monier-Williams')"
    )

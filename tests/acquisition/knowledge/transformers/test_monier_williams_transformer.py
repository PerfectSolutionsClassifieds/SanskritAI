
from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)
from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    MonierWilliamsTransformer,
)


# ============================================================
# Construction
# ============================================================

def test_default_transformer_metadata():
    transformer = MonierWilliamsTransformer()

    assert transformer.resource_name == "Monier-Williams"
    assert transformer.resource_version == "unknown"


# ============================================================
# Transformation
# ============================================================

def test_transform_creates_canonical_lexical_record():
    entry = RawLexicalEntry(
        source_name="Monier-Williams",
        source_version="1.0.0",
        source_record_id="agni",
        headword="agni",
        transliteration="agni",
        language="Sanskrit",
        script="Devanagari",
        raw_text="अग्निः fire",
        entry_type="noun",
        citation="MW",
        metadata={"page": 1},
    )

    transformer = MonierWilliamsTransformer()

    result = transformer.transform(entry)

    assert isinstance(result, CanonicalLexicalRecord)


def test_transform_maps_all_supported_fields():
    metadata = {
        "page": 123,
        "volume": "I",
    }

    entry = RawLexicalEntry(
        source_name="Monier-Williams",
        source_version="1.0.0",
        source_record_id="agni",
        headword=" agni ",
        transliteration="agni",
        language="Sanskrit",
        script="Devanagari",
        raw_text=" अग्निः fire ",
        entry_type="noun",
        citation="MW p.123",
        metadata=metadata,
    )

    transformer = MonierWilliamsTransformer()

    result = transformer.transform(entry)

    assert result.headword == "agni"
    assert result.transliteration == "agni"
    assert result.language == "Sanskrit"
    assert result.script == "Devanagari"
    assert result.definition == "अग्निः fire"
    assert result.entry_type == "noun"
    assert result.source_name == "Monier-Williams"
    assert result.source_version == "1.0.0"
    assert result.source_record_id == "agni"
    assert result.citation == "MW p.123"
    assert result.metadata == metadata


def test_transform_strips_headword():
    entry = RawLexicalEntry(
        source_name="Test",
        source_version="1.0",
        source_record_id="agni",
        headword="   agni   ",
        raw_text="fire",
    )

    transformer = MonierWilliamsTransformer()

    result = transformer.transform(entry)

    assert result.headword == "agni"


def test_transform_strips_raw_text_into_definition():
    entry = RawLexicalEntry(
        source_name="Test",
        source_version="1.0",
        source_record_id="agni",
        headword="agni",
        raw_text="   fire flame   ",
    )

    transformer = MonierWilliamsTransformer()

    result = transformer.transform(entry)

    assert result.definition == "fire flame"


def test_transform_copies_metadata():
    metadata = {
        "page": 10,
        "source": "MW",
    }

    entry = RawLexicalEntry(
        source_name="Test",
        source_version="1.0",
        source_record_id="agni",
        headword="agni",
        raw_text="fire",
        metadata=metadata,
    )

    transformer = MonierWilliamsTransformer()

    result = transformer.transform(entry)

    assert result.metadata == metadata
    assert result.metadata is not metadata

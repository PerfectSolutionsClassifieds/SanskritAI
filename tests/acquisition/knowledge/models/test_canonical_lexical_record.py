
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)


def test_canonical_lexical_record_creation():

    record = CanonicalLexicalRecord(
        headword="राम",
        transliteration="rāma",
        definition="A proper name",
        entry_type="noun",
        source_name="Monier-Williams",
        source_version="1.0",
        source_record_id="MW-001",
    )

    assert record.headword == "राम"
    assert record.transliteration == "rāma"
    assert record.definition == "A proper name"
    assert record.entry_type == "noun"
    assert record.source_name == "Monier-Williams"
    assert record.source_version == "1.0"
    assert record.source_record_id == "MW-001"


def test_canonical_lexical_record_defaults():

    record = CanonicalLexicalRecord(
        headword="राम",
    )

    assert record.transliteration is None
    assert record.language == "sa"
    assert record.script == "Devanagari"
    assert record.definition == ""
    assert record.entry_type is None
    assert record.source_name == ""
    assert record.source_version == ""
    assert record.source_record_id == ""
    assert record.citation is None
    assert record.metadata == {}


def test_summary():

    record = CanonicalLexicalRecord(
        headword="गम्",
        source_name="Dhātupāṭha",
        source_version="1.0",
        entry_type="dhātu",
    )

    assert record.summary() == {
        "headword": "गम्",
        "source": "Dhātupāṭha",
        "version": "1.0",
        "entry_type": "dhātu",
    }


def test_string_representation():

    record = CanonicalLexicalRecord(
        headword="गम्",
    )

    assert str(record) == "CanonicalLexicalRecord(गम्)"


def test_immutability():

    record = CanonicalLexicalRecord(
        headword="राम",
    )

    with pytest.raises(Exception):
        record.headword = "हरि"

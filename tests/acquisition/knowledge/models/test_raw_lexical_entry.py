
import pytest

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


def test_raw_lexical_entry_creation():

    entry = RawLexicalEntry(
        source_name="Monier-Williams",
        source_version="1.0",
        source_record_id="MW-001",
        headword="राम",
        raw_text="रामः",
    )

    assert entry.source_name == "Monier-Williams"
    assert entry.source_version == "1.0"
    assert entry.source_record_id == "MW-001"
    assert entry.headword == "राम"
    assert entry.raw_text == "रामः"


def test_raw_lexical_entry_defaults():

    entry = RawLexicalEntry(
        source_name="Apte",
        source_version="1.0",
        source_record_id="A-001",
    )

    assert entry.headword == ""
    assert entry.raw_text == ""
    assert entry.language == "sa"
    assert entry.script == "Devanagari"
    assert entry.transliteration is None
    assert entry.entry_type is None
    assert entry.section is None
    assert entry.metadata == {}


def test_has_headword():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1",
        source_record_id="1",
        headword="राम",
    )

    assert entry.has_headword is True


def test_has_headword_false_for_empty_or_whitespace():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1",
        source_record_id="1",
        headword="   ",
    )

    assert entry.has_headword is False


def test_has_raw_text():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1",
        source_record_id="1",
        raw_text="रामः पुत्रः",
    )

    assert entry.has_raw_text is True


def test_has_raw_text_false_for_empty_or_whitespace():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1",
        source_record_id="1",
        raw_text="   ",
    )

    assert entry.has_raw_text is False


def test_summary():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1.0",
        source_record_id="MW-001",
        headword="राम",
        language="sa",
        script="Devanagari",
        entry_type="noun",
    )

    result = entry.summary()

    assert result == {
        "source": "MW",
        "record_id": "MW-001",
        "headword": "राम",
        "script": "Devanagari",
        "language": "sa",
        "entry_type": "noun",
    }


def test_string_representation():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1.0",
        source_record_id="MW-001",
        headword="राम",
    )

    assert str(entry) == "RawLexicalEntry(MW: राम)"


def test_immutability():

    entry = RawLexicalEntry(
        source_name="MW",
        source_version="1",
        source_record_id="1",
        headword="राम",
    )

    with pytest.raises(Exception):
        entry.headword = "हरि"

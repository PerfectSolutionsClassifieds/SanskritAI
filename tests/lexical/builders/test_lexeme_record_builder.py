import pytest

from SanskritAI.lexical.builders.lexeme_record_builder import (
    LexemeRecordBuilder,
)
from SanskritAI.lexical.enums.dictionary_source import DictionarySource
from SanskritAI.lexical.enums.language import Language
from SanskritAI.lexical.enums.script import Script
from SanskritAI.lexical.records.lexeme_record import LexemeRecord


def make_record(**overrides) -> LexemeRecord:
    values = {
        "identifier": "lex-001",
        "lemma": "  धर्म  ",
        "normalized": "  धर्म  ",
        "dictionary": DictionarySource.AMARAKOSHA,
        "language": Language.SANSKRIT,
        "script": Script.DEVANAGARI,
        "devanagari": "  धर्म  ",
        "iast": "  dharma  ",
        "transliteration": "  dharma  ",
        "gloss": "  duty  ",
        "tags": ("noun", "abstract"),
        "notes": "  Editorial note.  ",
    }

    values.update(overrides)
    return LexemeRecord(**values)


def test_lexeme_record_builder_builds_lexeme():
    record = make_record()

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.identifier == "lex-001"
    assert lexeme.lemma == "धर्म"


def test_lexeme_record_builder_normalizes_lemma():
    record = make_record(lemma="   धर्म   ")

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.lemma == "धर्म"


def test_lexeme_record_builder_normalizes_optional_text():
    record = make_record(
        normalized="   धर्म   ",
        devanagari="   धर्म   ",
        iast="   dharma   ",
        transliteration="   dharma   ",
        gloss="   duty   ",
        notes="   note   ",
    )

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.metadata.extra["normalized"] == "धर्म"
    assert lexeme.metadata.extra["devanagari"] == "धर्म"
    assert lexeme.metadata.extra["iast"] == "dharma"
    assert lexeme.transliteration == "dharma"
    assert lexeme.metadata.extra["gloss"] == "duty"
    assert lexeme.metadata.extra["notes"] == "note"


def test_lexeme_record_builder_preserves_dictionary():
    record = make_record(
        dictionary=DictionarySource.AMARAKOSHA,
    )

    lexeme = LexemeRecordBuilder().build(record)

    assert (
        lexeme.metadata.extra["dictionary"]
        == DictionarySource.AMARAKOSHA
    )


def test_lexeme_record_builder_preserves_language():
    record = make_record(
        language=Language.SANSKRIT,
    )

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.language == Language.SANSKRIT


def test_lexeme_record_builder_preserves_script():
    record = make_record(
        script=Script.DEVANAGARI,
    )

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.script == Script.DEVANAGARI


def test_lexeme_record_builder_preserves_tags_as_tuple():
    record = make_record(tags=("noun", "abstract"))

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.metadata.extra["tags"] == (
        "noun",
        "abstract",
    )


def test_lexeme_record_builder_preserves_empty_optional_values():
    record = make_record(
        normalized="",
        devanagari="",
        iast="",
        transliteration="",
        gloss="",
        notes="",
    )

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.metadata.extra["normalized"] == ""
    assert lexeme.metadata.extra["devanagari"] == ""
    assert lexeme.metadata.extra["iast"] == ""
    assert lexeme.transliteration == ""
    assert lexeme.metadata.extra["gloss"] == ""
    assert lexeme.metadata.extra["notes"] == ""


def test_lexeme_record_builder_preserves_identifier():
    record = make_record(identifier="mw-dharma-001")

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.identifier == "mw-dharma-001"


def test_lexeme_record_builder_exposes_record_type():
    builder = LexemeRecordBuilder()

    assert builder.record_type is LexemeRecord


def test_lexeme_record_builder_rejects_wrong_record_type():
    builder = LexemeRecordBuilder()

    with pytest.raises(TypeError):
        builder.build("not-a-lexeme-record")


def test_lexeme_record_builder_returns_immutable_lexeme():
    record = make_record()

    lexeme = LexemeRecordBuilder().build(record)

    try:
        lexeme.identifier = "changed"
    except Exception:
        pass
    else:
        raise AssertionError("Lexeme must be immutable.")


def test_lexeme_record_builder_does_not_mutate_record():
    record = make_record()

    original_lemma = record.lemma
    original_gloss = record.gloss

    LexemeRecordBuilder().build(record)

    assert record.lemma == original_lemma
    assert record.gloss == original_gloss


def test_lexeme_record_builder_maps_all_record_information():
    record = make_record()

    lexeme = LexemeRecordBuilder().build(record)

    assert lexeme.identifier == "lex-001"
    assert lexeme.lemma == "धर्म"
    assert lexeme.transliteration == "dharma"
    assert lexeme.language == Language.SANSKRIT
    assert lexeme.script == Script.DEVANAGARI

    assert lexeme.metadata.extra == {
        "normalized": "धर्म",
        "dictionary": DictionarySource.AMARAKOSHA,
        "devanagari": "धर्म",
        "iast": "dharma",
        "gloss": "duty",
        "notes": "Editorial note.",
        "tags": ("noun", "abstract"),
    }

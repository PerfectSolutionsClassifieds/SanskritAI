from SanskritAI.lexical.builders.lexeme_builder import LexemeBuilder
from SanskritAI.lexical.enums.dictionary_source import DictionarySource
from SanskritAI.lexical.enums.language import Language
from SanskritAI.lexical.enums.script import Script
from SanskritAI.lexical.enums.part_of_speech import PartOfSpeech
from SanskritAI.lexical.models.lexeme import Lexeme


def test_lexeme_builder_builds_lexeme():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .build()
    )

    assert isinstance(lexeme, Lexeme)
    assert lexeme.identifier == "lex-001"
    assert lexeme.lemma == "धर्म"


def test_lexeme_builder_maps_transliteration():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_transliteration("dharma")
        .build()
    )

    assert lexeme.transliteration == "dharma"


def test_lexeme_builder_maps_part_of_speech():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_part_of_speech(PartOfSpeech.NOUN)
        .build()
    )

    assert lexeme.part_of_speech == PartOfSpeech.NOUN


def test_lexeme_builder_maps_root():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_root("धृ")
        .build()
    )

    assert lexeme.root == "धृ"


def test_lexeme_builder_maps_frequency():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_frequency(42)
        .build()
    )

    assert lexeme.frequency == 42


def test_lexeme_builder_maps_language():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_language(Language.SANSKRIT)
        .build()
    )

    assert lexeme.language == Language.SANSKRIT


def test_lexeme_builder_maps_script():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_script(Script.DEVANAGARI)
        .build()
    )

    assert lexeme.script == Script.DEVANAGARI


def test_lexeme_builder_maps_normalized_record_field():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_normalized("धर्म")
        .build()
    )

    assert lexeme.metadata.extra["normalized"] == "धर्म"


def test_lexeme_builder_maps_dictionary_record_field():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_dictionary(DictionarySource.AMARAKOSHA)
        .build()
    )

    assert lexeme.metadata.extra["dictionary"] == DictionarySource.AMARAKOSHA


def test_lexeme_builder_maps_devanagari():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("dharma")
        .with_devanagari("धर्म")
        .build()
    )

    assert lexeme.metadata.extra["devanagari"] == "धर्म"


def test_lexeme_builder_maps_iast():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_iast("dharma")
        .build()
    )

    assert lexeme.metadata.extra["iast"] == "dharma"


def test_lexeme_builder_maps_gloss():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_gloss("duty")
        .build()
    )

    assert lexeme.metadata.extra["gloss"] == "duty"


def test_lexeme_builder_maps_notes():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_notes("Editorial note")
        .build()
    )

    assert lexeme.metadata.extra["notes"] == "Editorial note"


def test_lexeme_builder_maps_tags():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_tags(["noun", "abstract"])
        .build()
    )

    assert lexeme.metadata.extra["tags"] == ("noun", "abstract")


def test_lexeme_builder_supports_fluent_chaining():
    builder = LexemeBuilder()

    result = (
        builder
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_transliteration("dharma")
        .with_root("धृ")
    )

    assert result is builder


def test_lexeme_builder_preserves_multiple_extra_fields():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_normalized("धर्म")
        .with_devanagari("धर्म")
        .with_iast("dharma")
        .with_gloss("duty")
        .with_notes("note")
        .with_tags(["noun"])
        .build()
    )

    assert lexeme.metadata.extra == {
        "normalized": "धर्म",
        "devanagari": "धर्म",
        "iast": "dharma",
        "gloss": "duty",
        "notes": "note",
        "tags": ("noun",),
    }


def test_lexeme_builder_produces_immutable_lexeme():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .build()
    )

    try:
        lexeme.identifier = "lex-002"
    except Exception:
        pass
    else:
        raise AssertionError("Lexeme must be immutable.")


def test_lexeme_builder_default_values_are_preserved():
    lexeme = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .build()
    )

    assert lexeme.transliteration == ""
    assert lexeme.root == ""
    assert lexeme.frequency == 0
    assert lexeme.metadata.extra == {}

import pytest
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata
from SanskritAI.lexical.enums.lexical_status import LexicalStatus
from SanskritAI.lexical.enums.part_of_speech import PartOfSpeech


def make_metadata():
    return LexemeMetadata.from_lemma(
        "धर्म",
        transliteration="dharma",
        language="sanskrit",
        script="devanagari",
        status=LexicalStatus.VERIFIED,
        part_of_speech=PartOfSpeech.NOUN,
        root="धृ",
        frequency=125,
        description="A canonical Sanskrit lexeme.",
    )


def make_lexeme():
    return Lexeme(
        identifier="lexeme-dharma",
        metadata=make_metadata(),
    )


def test_lexeme_stores_identifier():
    lexeme = make_lexeme()
    assert lexeme.identifier == "lexeme-dharma"


def test_lexeme_exposes_lemma():
    assert make_lexeme().lemma == "धर्म"


def test_lexeme_exposes_transliteration():
    assert make_lexeme().transliteration == "dharma"


def test_lexeme_exposes_part_of_speech():
    assert make_lexeme().part_of_speech == PartOfSpeech.NOUN


def test_lexeme_exposes_root():
    assert make_lexeme().root == "धृ"


def test_lexeme_exposes_frequency():
    assert make_lexeme().frequency == 125


def test_lexeme_exposes_language():
    assert make_lexeme().language == "sanskrit"


def test_lexeme_exposes_script():
    assert make_lexeme().script == "devanagari"


def test_lexeme_exposes_status():
    assert make_lexeme().status == LexicalStatus.VERIFIED


def test_lexeme_metadata_is_preserved():
    lexeme = make_lexeme()
    assert lexeme.metadata == make_metadata()


def test_lexeme_uses_canonical_identifier():
    lexeme = make_lexeme()
    assert str(lexeme.identifier) == "lexeme-dharma"


def test_lexeme_is_known_when_lemma_exists():
    assert make_lexeme().metadata.is_known is True


def test_lexeme_metadata_display_title_defaults_to_lemma():
    metadata = LexemeMetadata.from_lemma("गज")
    assert metadata.display_title == "गज"


def test_lexeme_metadata_can_have_explicit_title():
    metadata = LexemeMetadata(
        lemma="गज",
        title="Elephant",
    )
    assert metadata.display_title == "Elephant"


def test_lexeme_metadata_has_title():
    metadata = LexemeMetadata(
        lemma="गज",
        title="Elephant",
    )
    assert metadata.has_title is True

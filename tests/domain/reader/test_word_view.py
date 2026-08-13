from dataclasses import FrozenInstanceError
import pytest
from SanskritAI.domain.reader.word_view import WordView
from SanskritAI.domain.reader.reader_position import ReaderPosition
def make_position(word_id="word-1"):
    return ReaderPosition(purana_id="purana-1", chapter_id="chapter-1", sloka_id="sloka-1", word_id=word_id)
def make_word(surface="रामः", transliteration="", normalized="rāmaḥ"):
    return WordView(identifier="word-1", position=make_position(), title=surface, surface=surface, transliteration=transliteration, normalized=normalized)
def test_default_fields_are_empty():
    word = WordView(identifier="word-1", position=make_position(), title="रामः")
    assert word.surface == ""
    assert word.transliteration == ""
    assert word.normalized == ""
    assert word.has_transliteration is False
    assert word.has_normalized is False
def test_display_contract():
    word = make_word(surface="रामः")
    assert word.display_name == "Word"
    assert word.display_text == "रामः"
    assert word.display_description == "Immutable reader word."
    assert str(word) == "रामः"
def test_display_falls_back_to_reader_view():
    word = make_word(surface="")
    assert word.display_text == "word-1"
def test_transliteration_availability():
    assert make_word(transliteration="rāmaḥ").has_transliteration is True
    assert make_word(transliteration="").has_transliteration is False
def test_normalized_availability():
    assert make_word(normalized="rāmaḥ").has_normalized is True
    assert make_word(normalized="").has_normalized is False
def test_lexical_key_prefers_normalized_form():
    word = make_word(surface="रामः", normalized="rāmaḥ")
    assert word.lexical_key == "rāmaḥ"
def test_lexical_key_falls_back_to_surface():
    word = make_word(surface="रामः", normalized="")
    assert word.lexical_key == "रामः"
def test_word_position_helpers_are_inherited():
    word = make_word()
    assert word.corpus_id == "purana-1"
    assert word.purana_id == "purana-1"
    assert word.chapter_id == "chapter-1"
    assert word.sloka_id == "sloka-1"
    assert word.word_id == "word-1"
def test_word_is_immutable():
    word = make_word()
    with pytest.raises(FrozenInstanceError):
        word.surface = "शिवः"

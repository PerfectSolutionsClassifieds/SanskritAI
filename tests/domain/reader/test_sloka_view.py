from dataclasses import FrozenInstanceError
import pytest
from SanskritAI.domain.reader.sloka_view import SlokaView
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.word_view import WordView
def make_position(chapter_id="chapter-1", sloka_id="sloka-1", word_id=None):
    return ReaderPosition(purana_id="purana-1", chapter_id=chapter_id, sloka_id=sloka_id, word_id=word_id)
def make_word(identifier="word-1", sloka_id="sloka-1", surface="रामः"):
    return WordView(identifier=identifier, position=make_position(sloka_id=sloka_id, word_id=identifier), title=surface, surface=surface, normalized=surface)
def make_sloka(words=(), text="रामः गच्छति"):
    return SlokaView(identifier="sloka-1", position=make_position(), title="Sloka 1", words=tuple(words), sloka_text=text, translation="Rama goes.")
def test_default_words_are_empty():
    sloka = make_sloka()
    assert sloka.words == ()
    assert sloka.sloka_text == "रामः गच्छति"
    assert sloka.translation == "Rama goes."
    assert sloka.word_count == 0
    assert sloka.is_empty is True
    assert len(sloka) == 0
def test_words_are_preserved_in_order():
    first = make_word("word-1", surface="रामः")
    second = make_word("word-2", surface="गच्छति")
    sloka = make_sloka((first, second))
    assert sloka.words == (first, second)
    assert tuple(sloka) == (first, second)
    assert list(sloka) == [first, second]
    assert len(sloka) == 2
    assert sloka.word_count == 2
    assert sloka.is_empty is False
def test_index_access_returns_word():
    first = make_word("word-1")
    second = make_word("word-2")
    sloka = make_sloka((first, second))
    assert sloka[0] is first
    assert sloka[1] is second
def test_word_returns_matching_word():
    first = make_word("word-1")
    second = make_word("word-2")
    sloka = make_sloka((first, second))
    assert sloka.word("word-1") is first
    assert sloka.word("word-2") is second
def test_word_raises_for_unknown_identifier():
    sloka = make_sloka((make_word(),))
    with pytest.raises(KeyError, match="Unknown word 'missing'"):
        sloka.word("missing")
def test_contains_sloka_position():
    sloka = make_sloka((make_word(),))
    assert sloka.contains(make_position()) is True
def test_contains_word_position():
    sloka = make_sloka((make_word("word-1"),))
    assert sloka.contains(make_position(word_id="word-1")) is True
    assert sloka.contains(make_position(word_id="word-2")) is False
def test_contains_rejects_wrong_sloka():
    sloka = make_sloka((make_word(),))
    assert sloka.contains(make_position(sloka_id="sloka-2")) is False
def test_display_prefers_sloka_text():
    sloka = make_sloka(text="ॐ नमः शिवाय")
    assert sloka.display_name == "Śloka"
    assert sloka.display_text == "ॐ नमः शिवाय"
    assert sloka.display_description == "Immutable reader śloka."
def test_display_falls_back_to_title():
    sloka = make_sloka(text="")
    assert sloka.display_text == "Sloka 1"
def test_sloka_is_immutable():
    sloka = make_sloka()
    with pytest.raises(FrozenInstanceError):
        sloka.translation = "Changed"

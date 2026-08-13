from dataclasses import FrozenInstanceError
import pytest
from SanskritAI.domain.reader.chapter_view import ChapterView
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.sloka_view import SlokaView
def make_position(chapter_id="chapter-1", sloka_id=None, word_id=None):
    return ReaderPosition(purana_id="purana-1", chapter_id=chapter_id, sloka_id=sloka_id, word_id=word_id)
def make_sloka(identifier="sloka-1", chapter_id="chapter-1", text="श्लोकः"):
    return SlokaView(identifier=identifier, position=make_position(chapter_id, identifier), title=identifier, sloka_text=text)
def make_chapter(slokas=()):
    return ChapterView(identifier="chapter-1", position=make_position(), title="Chapter 1", slokas=tuple(slokas))
def test_default_slokas_are_empty():
    chapter = make_chapter()
    assert chapter.slokas == ()
    assert chapter.sloka_count == 0
    assert chapter.is_empty is True
    assert len(chapter) == 0
def test_slokas_are_preserved_in_order():
    first = make_sloka("sloka-1")
    second = make_sloka("sloka-2")
    chapter = make_chapter((first, second))
    assert chapter.slokas == (first, second)
    assert tuple(chapter) == (first, second)
    assert list(chapter) == [first, second]
    assert len(chapter) == 2
def test_index_access_returns_sloka():
    first = make_sloka("sloka-1")
    second = make_sloka("sloka-2")
    chapter = make_chapter((first, second))
    assert chapter[0] is first
    assert chapter[1] is second
def test_sloka_returns_matching_sloka():
    first = make_sloka("sloka-1")
    second = make_sloka("sloka-2")
    chapter = make_chapter((first, second))
    assert chapter.sloka("sloka-1") is first
    assert chapter.sloka("sloka-2") is second
def test_sloka_raises_for_unknown_identifier():
    chapter = make_chapter((make_sloka(),))
    with pytest.raises(KeyError, match="Unknown śloka 'missing'"):
        chapter.sloka("missing")
def test_contains_chapter_position():
    chapter = make_chapter((make_sloka(),))
    assert chapter.contains(make_position("chapter-1")) is True
    assert chapter.contains(make_position("chapter-2")) is False
def test_contains_matching_sloka_position():
    chapter = make_chapter((make_sloka("sloka-1"),))
    assert chapter.contains(make_position("chapter-1", "sloka-1")) is True
    assert chapter.contains(make_position("chapter-1", "sloka-2")) is False
def test_contains_rejects_wrong_chapter_even_with_matching_sloka():
    chapter = make_chapter((make_sloka("sloka-1"),))
    assert chapter.contains(make_position("chapter-2", "sloka-1")) is False
def test_display_contract():
    chapter = make_chapter()
    assert chapter.display_name == "Chapter"
    assert chapter.display_description == "Immutable reader chapter."
    assert chapter.display_text == "Chapter 1"
    assert str(chapter) == "Chapter 1"
def test_chapter_is_immutable():
    chapter = make_chapter()
    with pytest.raises(FrozenInstanceError):
        chapter.title = "Changed"

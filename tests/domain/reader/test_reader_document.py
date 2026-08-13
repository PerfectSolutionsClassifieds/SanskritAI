from dataclasses import FrozenInstanceError
import pytest
from SanskritAI.domain.reader.reader_document import ReaderDocument
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.chapter_view import ChapterView
def make_position(chapter_id="chapter-1", sloka_id=None, word_id=None):
    return ReaderPosition(purana_id="purana-1", chapter_id=chapter_id, sloka_id=sloka_id, word_id=word_id)
def make_chapter(identifier="chapter-1", title="Chapter 1"):
    return ChapterView(identifier=identifier, position=make_position(identifier), title=title)
def make_document(chapters=()):
    return ReaderDocument(identifier="document-1", position=make_position(), title="Document", chapters=tuple(chapters))
def test_default_chapters_are_empty():
    document = make_document()
    assert document.chapters == ()
    assert document.chapter_count == 0
    assert document.is_empty is True
    assert len(document) == 0
def test_chapters_are_preserved_in_order():
    first = make_chapter("chapter-1")
    second = make_chapter("chapter-2")
    document = make_document((first, second))
    assert document.chapters == (first, second)
    assert tuple(document) == (first, second)
    assert list(document) == [first, second]
    assert len(document) == 2
def test_chapter_returns_matching_chapter():
    first = make_chapter("chapter-1")
    second = make_chapter("chapter-2")
    document = make_document((first, second))
    assert document.chapter("chapter-1") is first
    assert document.chapter("chapter-2") is second
def test_chapter_raises_for_unknown_identifier():
    document = make_document((make_chapter(),))
    with pytest.raises(KeyError, match="Unknown chapter 'missing'"):
        document.chapter("missing")
def test_contains_matches_chapter_position():
    document = make_document((make_chapter("chapter-1"),))
    assert document.contains(make_position("chapter-1")) is True
    assert document.contains(make_position("chapter-2")) is False
def test_contains_accepts_deeper_position_in_existing_chapter():
    document = make_document((make_chapter("chapter-1"),))
    position = make_position("chapter-1", "sloka-1", "word-1")
    assert document.contains(position) is True
def test_display_contract():
    document = make_document()
    assert document.display_name == "Reader Document"
    assert document.display_description == "Immutable reader document."
    assert document.display_text == "Document"
    assert str(document) == "Document"
def test_reader_document_is_immutable():
    document = make_document()
    with pytest.raises(FrozenInstanceError):
        document.title = "Changed"
def test_reader_document_is_value_object():
    document = make_document()
    assert isinstance(document, ReaderDocument)

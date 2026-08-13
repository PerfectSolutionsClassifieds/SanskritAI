from __future__ import annotations
import pytest
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext

def make_position(level: str = "word") -> ReaderPosition:
    if level == "purana":
        return ReaderPosition(purana_id="corpus-1")
    if level == "chapter":
        return ReaderPosition(purana_id="corpus-1", chapter_id="chapter-1")
    if level == "sloka":
        return ReaderPosition(purana_id="corpus-1", chapter_id="chapter-1", sloka_id="sloka-1")
    return ReaderPosition(purana_id="corpus-1", chapter_id="chapter-1", sloka_id="sloka-1", word_id="word-1")

def test_reader_selection_context_from_position():
    position = make_position("word")
    context = ReaderSelectionContext.from_position(position)
    assert context.position is position

def test_reader_selection_context_exposes_position_identifiers():
    context = ReaderSelectionContext.from_position(make_position("word"))
    assert context.purana_id == "corpus-1"
    assert context.chapter_id == "chapter-1"
    assert context.sloka_id == "sloka-1"
    assert context.word_id == "word-1"

def test_reader_selection_context_exposes_position_state():
    context = ReaderSelectionContext.from_position(make_position("word"))
    assert context.level == context.position.level
    assert context.canonical_id == context.position.canonical_id
    assert context.identifier == context.position.identifier
    assert context.is_purana is context.position.is_purana
    assert context.is_chapter is context.position.is_chapter
    assert context.is_sloka is context.position.is_sloka
    assert context.is_word is context.position.is_word

def test_reader_selection_context_has_hierarchy_flags():
    assert ReaderSelectionContext.from_position(make_position("purana")).has_chapter is False
    assert ReaderSelectionContext.from_position(make_position("purana")).has_sloka is False
    assert ReaderSelectionContext.from_position(make_position("purana")).has_word is False
    assert ReaderSelectionContext.from_position(make_position("chapter")).has_chapter is True
    assert ReaderSelectionContext.from_position(make_position("chapter")).has_sloka is False
    assert ReaderSelectionContext.from_position(make_position("chapter")).has_word is False
    assert ReaderSelectionContext.from_position(make_position("sloka")).has_chapter is True
    assert ReaderSelectionContext.from_position(make_position("sloka")).has_sloka is True
    assert ReaderSelectionContext.from_position(make_position("sloka")).has_word is False
    assert ReaderSelectionContext.from_position(make_position("word")).has_chapter is True
    assert ReaderSelectionContext.from_position(make_position("word")).has_sloka is True
    assert ReaderSelectionContext.from_position(make_position("word")).has_word is True

def test_reader_selection_context_to_position_returns_canonical_position():
    position = make_position("word")
    context = ReaderSelectionContext(position=position)
    assert context.to_position() is position
    assert context.to_position() == position

def test_reader_selection_context_display_contract():
    context = ReaderSelectionContext.from_position(make_position("word"))
    assert context.display_name == "Reader Selection Context"
    assert context.display_text == str(context.position)
    assert context.display_description == "Immutable context describing the current Reader selection."
    assert str(context) == context.display_text

def test_reader_selection_context_is_immutable():
    context = ReaderSelectionContext.from_position(make_position("word"))
    with pytest.raises((AttributeError, TypeError)):
        context.position = make_position("chapter")

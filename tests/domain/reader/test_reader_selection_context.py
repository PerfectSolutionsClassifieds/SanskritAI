from __future__ import annotations
import pytest
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext

def make_position(level: str = "word") -> ReaderPosition:
    if level == "purana":
        return ReaderPosition(purana_id="corpus-1")
    if level == "chapter":
        return ReaderPosition(
            purana_id="corpus-1",
            chapter_id="chapter-1",
        )
    if level == "sloka":
        return ReaderPosition(
            purana_id="corpus-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        )
    if level == "word":
        return ReaderPosition(
            purana_id="corpus-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        )
    raise ValueError(f"Unknown test position level: {level}")

def test_reader_selection_context_from_position():
    position = make_position("word")
    context = ReaderSelectionContext.from_position(position)
    assert context.position is position

@pytest.mark.parametrize(
    "level",
    ["purana", "chapter", "sloka", "word"],
)
def test_reader_selection_context_preserves_position(level):
    position = make_position(level)
    context = ReaderSelectionContext.from_position(position)
    assert context.position is position
    assert context.to_position() is position
    assert context.to_position() == position

@pytest.mark.parametrize(
    "level",
    ["purana", "chapter", "sloka", "word"],
)
def test_reader_selection_context_exposes_identifiers(level):
    context = ReaderSelectionContext.from_position(make_position(level))
    assert context.purana_id == "corpus-1"
    if level == "purana":
        assert context.chapter_id is None
        assert context.sloka_id is None
        assert context.word_id is None
    elif level == "chapter":
        assert context.chapter_id == "chapter-1"
        assert context.sloka_id is None
        assert context.word_id is None
    elif level == "sloka":
        assert context.chapter_id == "chapter-1"
        assert context.sloka_id == "sloka-1"
        assert context.word_id is None
    else:
        assert context.chapter_id == "chapter-1"
        assert context.sloka_id == "sloka-1"
        assert context.word_id == "word-1"

@pytest.mark.parametrize(
    "level",
    ["purana", "chapter", "sloka", "word"],
)
def test_reader_selection_context_delegates_state_to_position(level):
    position = make_position(level)
    context = ReaderSelectionContext.from_position(position)
    assert context.level == position.level
    assert context.canonical_id == position.canonical_id
    assert context.identifier == position.identifier
    assert context.is_purana is position.is_purana
    assert context.is_chapter is position.is_chapter
    assert context.is_sloka is position.is_sloka
    assert context.is_word is position.is_word

def test_reader_selection_context_purana_hierarchy_flags():
    context = ReaderSelectionContext.from_position(make_position("purana"))
    assert context.has_chapter is False
    assert context.has_sloka is False
    assert context.has_word is False

def test_reader_selection_context_chapter_hierarchy_flags():
    context = ReaderSelectionContext.from_position(make_position("chapter"))
    assert context.has_chapter is True
    assert context.has_sloka is False
    assert context.has_word is False

def test_reader_selection_context_sloka_hierarchy_flags():
    context = ReaderSelectionContext.from_position(make_position("sloka"))
    assert context.has_chapter is True
    assert context.has_sloka is True
    assert context.has_word is False

def test_reader_selection_context_word_hierarchy_flags():
    context = ReaderSelectionContext.from_position(make_position("word"))
    assert context.has_chapter is True
    assert context.has_sloka is True
    assert context.has_word is True

def test_reader_selection_context_display_contract():
    context = ReaderSelectionContext.from_position(make_position("word"))
    assert context.display_name == "Reader Selection Context"
    assert context.display_text == str(context.position)
    assert context.display_description == (
        "Immutable context describing the current Reader selection."
    )
    assert str(context) == context.display_text

def test_reader_selection_context_is_immutable():
    context = ReaderSelectionContext.from_position(make_position("word"))
    with pytest.raises((AttributeError, TypeError)):
        context.position = make_position("chapter")

def test_reader_selection_context_is_frozen():
    context = ReaderSelectionContext.from_position(make_position("chapter"))
    with pytest.raises((AttributeError, TypeError)):
        context.chapter_id = "chapter-2"

def test_reader_selection_context_requires_position():
    with pytest.raises((TypeError, ValueError)):
        ReaderSelectionContext()

def test_reader_selection_context_accepts_direct_position_construction():
    position = make_position("chapter")
    context = ReaderSelectionContext(position=position)
    assert context.position is position
    assert context.chapter_id == "chapter-1"

def test_reader_selection_context_is_value_object_equal_by_value():
    first = ReaderSelectionContext.from_position(make_position("word"))
    second = ReaderSelectionContext.from_position(make_position("word"))
    assert first == second
    assert hash(first) == hash(second)

def test_reader_selection_context_distinguishes_different_positions():
    first = ReaderSelectionContext.from_position(make_position("chapter"))
    second = ReaderSelectionContext.from_position(make_position("sloka"))
    assert first != second

def test_reader_selection_context_does_not_navigate():
    context = ReaderSelectionContext.from_position(make_position("chapter"))
    assert not hasattr(context, "next")
    assert not hasattr(context, "previous")
    assert not hasattr(context, "move_next")
    assert not hasattr(context, "move_previous")
    assert not hasattr(context, "back")
    assert not hasattr(context, "forward")

def test_reader_selection_context_does_not_manage_history():
    context = ReaderSelectionContext.from_position(make_position("word"))
    assert not hasattr(context, "history")
    assert not hasattr(context, "back")
    assert not hasattr(context, "forward")

@pytest.mark.parametrize(
    "level,expected_level",
    [
        ("purana", "purana"),
        ("chapter", "chapter"),
        ("sloka", "sloka"),
        ("word", "word"),
    ],
)
def test_reader_selection_context_level_is_canonical(
    level,
    expected_level,
):
    context = ReaderSelectionContext.from_position(make_position(level))
    assert context.level == expected_level

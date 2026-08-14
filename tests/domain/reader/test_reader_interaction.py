from SanskritAI.domain.reader.reader_interaction import ReaderHoverContext
from SanskritAI.domain.reader.reader_interaction import ReaderInteraction
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext
def make_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )
def test_hover_creates_hover_context():
    position = make_position()
    result = ReaderInteraction.hover(position)
    assert isinstance(result, ReaderHoverContext)
    assert result.position is position
def test_hover_preserves_position():
    position = make_position()
    result = ReaderInteraction.hover(position)
    assert result.to_position() is position
def test_hover_exposes_hierarchy():
    result = ReaderInteraction.hover(make_position())
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert result.word_id == "word-1"
    assert result.level == "word"
def test_hover_exposes_canonical_id():
    position = make_position()
    result = ReaderInteraction.hover(position)
    assert result.canonical_id == position.canonical_id
def test_hover_is_immutable():
    result = ReaderInteraction.hover(make_position())
    try:
        result.position = make_position()
        raised = False
    except Exception:
        raised = True
    assert raised
def test_hover_does_not_change_position():
    position = make_position()
    result = ReaderInteraction.hover(position)
    assert result.position == position
def test_select_creates_selection_context():
    position = make_position()
    result = ReaderInteraction.select(position)
    assert isinstance(result, ReaderSelectionContext)
def test_select_preserves_position():
    position = make_position()
    result = ReaderInteraction.select(position)
    assert result.position is position
def test_select_exposes_hierarchy():
    result = ReaderInteraction.select(make_position())
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert result.word_id == "word-1"
def test_select_exposes_level():
    result = ReaderInteraction.select(make_position())
    assert result.level == "word"
def test_select_exposes_canonical_id():
    position = make_position()
    result = ReaderInteraction.select(position)
    assert result.canonical_id == position.canonical_id
def test_select_can_be_converted_back_to_position():
    position = make_position()
    result = ReaderInteraction.select(position)
    assert result.to_position() is position
def test_selection_is_immutable():
    result = ReaderInteraction.select(make_position())
    try:
        result.position = make_position()
        raised = False
    except Exception:
        raised = True
    assert raised
def test_hover_and_selection_are_distinct_contexts():
    position = make_position()
    hover = ReaderInteraction.hover(position)
    selection = ReaderInteraction.select(position)
    assert hover is not selection
    assert hover.position is selection.position
def test_hover_does_not_create_selection():
    position = make_position()
    hover = ReaderInteraction.hover(position)
    assert isinstance(hover, ReaderHoverContext)
    assert not isinstance(hover, ReaderSelectionContext)

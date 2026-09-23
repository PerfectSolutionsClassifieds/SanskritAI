from __future__ import annotations
"""
SanskritAI
==========
ReaderNavigator Tests
Verifies canonical-ID navigation, ReaderPositionFactory integration,
structural context preservation, validation, immutability, and the
identifier-based navigation contract.
The tests intentionally use a repository stub so Navigator behavior
is tested independently from Corpus construction.
Version
-------
v3.1.1
"""
from dataclasses import dataclass
import pytest
from SanskritAI.domain.reader.reader_navigator import ReaderNavigator
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_position_factory import ReaderPositionFactory

# =============================================================
# Test Objects
# =============================================================
@dataclass(frozen=True)
class FakeView:
    identifier: str
    position: ReaderPosition

class FakeRepository:
    """Minimal ReaderRepository-compatible test double."""
    def __init__(self):
        self.calls = []
        self.chapters = {
            "chapter-1": FakeView("chapter-1",ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-1")),
            "chapter-2": FakeView("chapter-2",ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-2")),
            "chapter-3": FakeView("chapter-3",ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-3")),
        }
        self.slokas = {
            "sloka-1": FakeView("sloka-1",ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1")),
            "sloka-2": FakeView("sloka-2",ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-2")),
            "sloka-3": FakeView("sloka-3",ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-3")),
        }
        self.words = {
            "word-1": FakeView("word-1",ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-1")),
            "word-2": FakeView("word-2",ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-2")),
            "word-3": FakeView("word-3",ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-3")),
        }

    def next_chapter(self,chapter_id):
        self.calls.append(("next_chapter",chapter_id))
        order=["chapter-1","chapter-2","chapter-3"]
        try:index=order.index(str(chapter_id))
        except ValueError:raise KeyError(chapter_id)
        return None if index+1>=len(order) else self.chapters[order[index+1]]

    def previous_chapter(self,chapter_id):
        self.calls.append(("previous_chapter",chapter_id))
        order=["chapter-1","chapter-2","chapter-3"]
        try:index=order.index(str(chapter_id))
        except ValueError:raise KeyError(chapter_id)
        return None if index==0 else self.chapters[order[index-1]]

    # def next_sloka(self,sloka_id):
    #     self.calls.append(("next_sloka",sloka_id))
    #     order=["sloka-1","sloka-2","sloka-3"]
    #     index=order.index(str(sloka_id))
    #     return None if index+1>=len(order) else self.slokas[order[index+1]]

    def next_sloka(self,sloka_id):
        self.calls.append(("next_sloka",sloka_id))
        order=["sloka-1","sloka-2","sloka-3"]
        key=str(sloka_id)
        if key not in order:
            raise KeyError(key)
        index=order.index(key)
        return None if index+1>=len(order) else self.slokas[order[index+1]]

    def previous_sloka(self,sloka_id):
        self.calls.append(("previous_sloka",sloka_id))
        order=["sloka-1","sloka-2","sloka-3"]
        index=order.index(str(sloka_id))
        return None if index==0 else self.slokas[order[index-1]]

    def next_word(self,word_id):
        self.calls.append(("next_word",word_id))
        order=["word-1","word-2","word-3"]
        index=order.index(str(word_id))
        return None if index+1>=len(order) else self.words[order[index+1]]

    def previous_word(self,word_id):
        self.calls.append(("previous_word",word_id))
        order=["word-1","word-2","word-3"]
        index=order.index(str(word_id))
        return None if index==0 else self.words[order[index-1]]

class RecordingPositionFactory(ReaderPositionFactory):
    """Factory double proving that Navigator uses the injected factory."""
    pass

# =============================================================
# Fixtures
# =============================================================
@pytest.fixture
def repository():
    return FakeRepository()

@pytest.fixture
def navigator(repository):
    return ReaderNavigator(repository=repository,position_factory=ReaderPositionFactory())

def make_navigator():
    repository=FakeRepository()
    navigator=ReaderNavigator(repository=repository,position_factory=ReaderPositionFactory())
    return navigator,repository

# =============================================================
# Chapter Tests
# =============================================================
def test_next_chapter_uses_canonical_id():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-1")
    result=navigator.next_chapter(current)
    assert result is not None
    assert result.purana_id=="purana-1"
    assert result.chapter_id=="chapter-2"
    assert repository.calls[-1]==("next_chapter","chapter-1")

def test_previous_chapter_uses_canonical_id():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-2")
    result=navigator.previous_chapter(current)
    assert result is not None
    assert result.purana_id=="purana-1"
    assert result.chapter_id=="chapter-1"
    assert repository.calls[-1]==("previous_chapter","chapter-2")

def test_first_chapter_has_no_previous():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-1")
    assert navigator.previous_chapter(current) is None

def test_last_chapter_has_no_next():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-3")
    assert navigator.next_chapter(current) is None

def test_next_chapter_rejects_missing_chapter_context():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.purana(purana_id="purana-1")
    with pytest.raises(ValueError,match="chapter_id"):
        navigator.next_chapter(current)

def test_previous_chapter_rejects_missing_chapter_context():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.purana(purana_id="purana-1")
    with pytest.raises(ValueError,match="chapter_id"):
        navigator.previous_chapter(current)

# =============================================================
# Śloka Tests
# =============================================================
def test_next_sloka_constructs_factory_position():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1")
    result=navigator.next_sloka(current)
    assert result is not None
    assert result.purana_id=="purana-1"
    assert result.chapter_id=="chapter-1"
    assert result.sloka_id=="sloka-2"
    assert repository.calls[-1]==("next_sloka","sloka-1")

def test_previous_sloka_constructs_factory_position():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-2")
    result=navigator.previous_sloka(current)
    assert result is not None
    assert result.purana_id=="purana-1"
    assert result.chapter_id=="chapter-1"
    assert result.sloka_id=="sloka-1"
    assert repository.calls[-1]==("previous_sloka","sloka-2")

def test_first_sloka_has_no_previous():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1")
    assert navigator.previous_sloka(current) is None

def test_last_sloka_has_no_next():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-3")
    assert navigator.next_sloka(current) is None

def test_next_sloka_rejects_missing_sloka_context():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-1")
    with pytest.raises(ValueError,match="sloka_id"):
        navigator.next_sloka(current)

def test_previous_sloka_rejects_missing_sloka_context():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-1")
    with pytest.raises(ValueError,match="sloka_id"):
        navigator.previous_sloka(current)

# =============================================================
# Word Tests
# =============================================================
def test_next_word_preserves_structural_context():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-1")
    result=navigator.next_word(current)
    assert result is not None
    assert result.purana_id=="purana-1"
    assert result.chapter_id=="chapter-1"
    assert result.sloka_id=="sloka-1"
    assert result.word_id=="word-2"
    assert repository.calls[-1]==("next_word","word-1")

def test_previous_word_preserves_structural_context():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-2")
    result=navigator.previous_word(current)
    assert result is not None
    assert result.purana_id=="purana-1"
    assert result.chapter_id=="chapter-1"
    assert result.sloka_id=="sloka-1"
    assert result.word_id=="word-1"
    assert repository.calls[-1]==("previous_word","word-2")

def test_first_word_has_no_previous():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-1")
    assert navigator.previous_word(current) is None

def test_last_word_has_no_next():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-3")
    assert navigator.next_word(current) is None

def test_next_word_rejects_missing_word_context():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1")
    with pytest.raises(ValueError,match="word_id"):
        navigator.next_word(current)

def test_previous_word_rejects_missing_word_context():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1")
    with pytest.raises(ValueError,match="word_id"):
        navigator.previous_word(current)

# =============================================================
# Position Construction / Factory Contract
# =============================================================
def test_navigation_returns_new_immutable_position():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="chapter-1")
    result=navigator.next_chapter(current)
    assert result is not None
    assert result is not current
    with pytest.raises(Exception):
        result.chapter_id="chapter-x"

def test_navigator_does_not_require_indices():
    navigator,_=make_navigator()
    position=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1")
    assert not hasattr(position,"chapter_index")
    assert not hasattr(position,"sloka_index")
    assert not hasattr(position,"word_index")
    result=navigator.next_sloka(position)
    assert result is not None
    assert result.sloka_id=="sloka-2"

def test_navigator_preserves_current_purana_id():
    navigator,repository=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-custom",chapter_id="chapter-1")
    result=navigator.next_chapter(current)
    assert result is not None
    assert result.purana_id=="purana-custom"
    assert repository.calls[-1]==("next_chapter","chapter-1")

def test_sloka_navigation_preserves_current_purana_id():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-custom",chapter_id="chapter-1",sloka_id="sloka-1")
    result=navigator.next_sloka(current)
    assert result is not None
    assert result.purana_id=="purana-custom"

def test_word_navigation_preserves_current_purana_id():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.word(purana_id="purana-custom",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-1")
    result=navigator.next_word(current)
    assert result is not None
    assert result.purana_id=="purana-custom"

def test_sloka_navigation_uses_view_structural_context():
    navigator,repository=make_navigator()
    repository.slokas["sloka-2"]=FakeView("sloka-2",ReaderPositionFactory.sloka(purana_id="purana-view",chapter_id="chapter-2",sloka_id="sloka-2"))
    current=ReaderPositionFactory.sloka(purana_id="purana-current",chapter_id="chapter-1",sloka_id="sloka-1")
    result=navigator.next_sloka(current)
    assert result is not None
    assert result.purana_id=="purana-current"
    assert result.chapter_id=="chapter-2"
    assert result.sloka_id=="sloka-2"

def test_word_navigation_uses_view_structural_context():
    navigator,repository=make_navigator()
    repository.words["word-2"]=FakeView("word-2",ReaderPositionFactory.word(purana_id="purana-view",chapter_id="chapter-2",sloka_id="sloka-2",word_id="word-2"))
    current=ReaderPositionFactory.word(purana_id="purana-current",chapter_id="chapter-1",sloka_id="sloka-1",word_id="word-1")
    result=navigator.next_word(current)
    assert result is not None
    assert result.purana_id=="purana-current"
    assert result.chapter_id=="chapter-2"
    assert result.sloka_id=="sloka-2"
    assert result.word_id=="word-2"

# =============================================================
# Repository Error Propagation
# =============================================================
def test_unknown_chapter_id_is_propagated():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id="unknown")
    with pytest.raises(KeyError):
        navigator.next_chapter(current)

def test_unknown_sloka_id_is_propagated():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id="unknown")
    with pytest.raises(KeyError):
        navigator.next_sloka(current)

def test_unknown_word_id_is_propagated():
    navigator,_=make_navigator()
    current=ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id="unknown")
    with pytest.raises(ValueError):
        navigator.next_word(current)

# =============================================================
# Injected Factory Contract
# =============================================================
def test_navigator_accepts_injected_position_factory():
    repository=FakeRepository()
    factory=ReaderPositionFactory()
    navigator=ReaderNavigator(repository=repository,position_factory=factory)
    assert navigator.position_factory is factory

def test_navigator_default_position_factory_is_available():
    repository=FakeRepository()
    navigator=ReaderNavigator(repository=repository)
    assert isinstance(navigator.position_factory,ReaderPositionFactory)

# =============================================================
# Position Helper Contract
# =============================================================
def test_require_chapter_id_returns_string():
    position=ReaderPositionFactory.chapter(purana_id="purana-1",chapter_id=123)
    assert ReaderNavigator._require_chapter_id(position)=="123"

def test_require_sloka_id_returns_string():
    position=ReaderPositionFactory.sloka(purana_id="purana-1",chapter_id="chapter-1",sloka_id=123)
    assert ReaderNavigator._require_sloka_id(position)=="123"

def test_require_word_id_returns_string():
    position=ReaderPositionFactory.word(purana_id="purana-1",chapter_id="chapter-1",sloka_id="sloka-1",word_id=123)
    assert ReaderNavigator._require_word_id(position)=="123"

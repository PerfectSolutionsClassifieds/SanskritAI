from __future__ import annotations
"""
SanskritAI
==========
ReaderNavigator Tests
Verifies canonical-ID navigation, ReaderPositionFactory integration,
position validation, structural-context fallback, factory injection,
and identifier-based navigation without positional indices.
The tests intentionally use repository stubs so Navigator behavior is
tested independently from Corpus construction.
Version
-------
v3.1.1
"""
from dataclasses import dataclass
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
            "chapter-1": FakeView(
                "chapter-1",
                ReaderPositionFactory.chapter(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                ),
            ),
            "chapter-2": FakeView(
                "chapter-2",
                ReaderPositionFactory.chapter(
                    purana_id="purana-1",
                    chapter_id="chapter-2",
                ),
            ),
            "chapter-3": FakeView(
                "chapter-3",
                ReaderPositionFactory.chapter(
                    purana_id="purana-1",
                    chapter_id="chapter-3",
                ),
            ),
        }
        self.slokas = {
            "sloka-1": FakeView(
                "sloka-1",
                ReaderPositionFactory.sloka(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                ),
            ),
            "sloka-2": FakeView(
                "sloka-2",
                ReaderPositionFactory.sloka(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-2",
                ),
            ),
            "sloka-3": FakeView(
                "sloka-3",
                ReaderPositionFactory.sloka(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-3",
                ),
            ),
        }
        self.words = {
            "word-1": FakeView(
                "word-1",
                ReaderPositionFactory.word(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                    word_id="word-1",
                ),
            ),
            "word-2": FakeView(
                "word-2",
                ReaderPositionFactory.word(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                    word_id="word-2",
                ),
            ),
            "word-3": FakeView(
                "word-3",
                ReaderPositionFactory.word(
                    purana_id="purana-1",
                    chapter_id="chapter-1",
                    sloka_id="sloka-1",
                    word_id="word-3",
                ),
            ),
        }

    # ---------------------------------------------------------
    # Chapter
    # ---------------------------------------------------------
    def next_chapter(self, chapter_id):
        self.calls.append(("next_chapter", chapter_id))
        order = ["chapter-1", "chapter-2", "chapter-3"]
        try:
            index = order.index(str(chapter_id))
        except ValueError:
            raise KeyError(chapter_id)
        if index + 1 >= len(order):
            return None
        return self.chapters[order[index + 1]]

    def previous_chapter(self, chapter_id):
        self.calls.append(("previous_chapter", chapter_id))
        order = ["chapter-1", "chapter-2", "chapter-3"]
        try:
            index = order.index(str(chapter_id))
        except ValueError:
            raise KeyError(chapter_id)
        if index == 0:
            return None
        return self.chapters[order[index - 1]]

    # ---------------------------------------------------------
    # Śloka
    # ---------------------------------------------------------
    def next_sloka(self, sloka_id):
        self.calls.append(("next_sloka", sloka_id))
        order = ["sloka-1", "sloka-2", "sloka-3"]
        index = order.index(str(sloka_id))
        if index + 1 >= len(order):
            return None
        return self.slokas[order[index + 1]]

    def previous_sloka(self, sloka_id):
        self.calls.append(("previous_sloka", sloka_id))
        order = ["sloka-1", "sloka-2", "sloka-3"]
        index = order.index(str(sloka_id))
        if index == 0:
            return None
        return self.slokas[order[index - 1]]

    # ---------------------------------------------------------
    # Word
    # ---------------------------------------------------------
    def next_word(self, word_id):
        self.calls.append(("next_word", word_id))
        order = ["word-1", "word-2", "word-3"]
        index = order.index(str(word_id))
        if index + 1 >= len(order):
            return None
        return self.words[order[index + 1]]

    def previous_word(self, word_id):
        self.calls.append(("previous_word", word_id))
        order = ["word-1", "word-2", "word-3"]
        index = order.index(str(word_id))
        if index == 0:
            return None
        return self.words[order[index - 1]]

# =============================================================
# Test Factory
# =============================================================
class SpyPositionFactory:
    """Factory spy used to verify ReaderNavigator factory injection."""
    def __init__(self):
        self.calls = []

    def purana(self, *, purana_id):
        self.calls.append(("purana", purana_id))
        return ReaderPositionFactory.purana(purana_id=purana_id)

    def chapter(self, *, purana_id, chapter_id):
        self.calls.append(("chapter", purana_id, chapter_id))
        return ReaderPositionFactory.chapter(
            purana_id=purana_id,
            chapter_id=chapter_id,
        )

    def sloka(self, *, purana_id, chapter_id, sloka_id):
        self.calls.append(("sloka", purana_id, chapter_id, sloka_id))
        return ReaderPositionFactory.sloka(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
        )

    def word(self, *, purana_id, chapter_id, sloka_id, word_id):
        self.calls.append(
            ("word", purana_id, chapter_id, sloka_id, word_id)
        )
        return ReaderPositionFactory.word(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=word_id,
        )

# =============================================================
# Fixtures
# =============================================================
def make_navigator(position_factory=None):
    repository = FakeRepository()
    if position_factory is None:
        position_factory = ReaderPositionFactory()
    navigator = ReaderNavigator(
        repository=repository,
        position_factory=position_factory,
    )
    return navigator, repository

def make_default_navigator():
    repository = FakeRepository()
    navigator = ReaderNavigator(
        repository=repository,
    )
    return navigator, repository

# =============================================================
# Chapter Tests
# =============================================================
def test_next_chapter_uses_canonical_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    result = navigator.next_chapter(current)
    assert result is not None
    assert result.chapter_id == "chapter-2"
    assert result.purana_id == "purana-1"
    assert repository.calls[-1] == ("next_chapter", "chapter-1")

def test_previous_chapter_uses_canonical_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )
    result = navigator.previous_chapter(current)
    assert result is not None
    assert result.chapter_id == "chapter-1"
    assert result.purana_id == "purana-1"
    assert repository.calls[-1] == ("previous_chapter", "chapter-2")

def test_first_chapter_has_no_previous():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    assert navigator.previous_chapter(current) is None

def test_last_chapter_has_no_next():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-3",
    )
    assert navigator.next_chapter(current) is None

def test_next_chapter_preserves_current_purana_id():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-custom",
        chapter_id="chapter-1",
    )
    result = navigator.next_chapter(current)
    assert result is not None
    assert result.purana_id == "purana-custom"
    assert result.chapter_id == "chapter-2"

def test_next_chapter_requires_chapter_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.purana(
        purana_id="purana-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="ReaderPosition does not contain a chapter_id.",
    ):
        navigator.next_chapter(current)
    assert repository.calls == []

def test_previous_chapter_requires_chapter_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.purana(
        purana_id="purana-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="ReaderPosition does not contain a chapter_id.",
    ):
        navigator.previous_chapter(current)
    assert repository.calls == []

# =============================================================
# Śloka Tests
# =============================================================
def test_next_sloka_constructs_factory_position():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    result = navigator.next_sloka(current)
    assert result is not None
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-2"
    assert repository.calls[-1] == ("next_sloka", "sloka-1")

def test_previous_sloka_constructs_factory_position():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-2",
    )
    result = navigator.previous_sloka(current)
    assert result is not None
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert repository.calls[-1] == ("previous_sloka", "sloka-2")

def test_first_sloka_has_no_previous():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    assert navigator.previous_sloka(current) is None

def test_last_sloka_has_no_next():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-3",
    )
    assert navigator.next_sloka(current) is None

def test_next_sloka_requires_sloka_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="ReaderPosition does not contain a sloka_id.",
    ):
        navigator.next_sloka(current)
    assert repository.calls == []

def test_previous_sloka_requires_sloka_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="ReaderPosition does not contain a sloka_id.",
    ):
        navigator.previous_sloka(current)
    assert repository.calls == []

def test_next_sloka_preserves_cross_chapter_context_from_target_view():
    navigator, repository = make_navigator()
    repository.slokas["sloka-2"] = FakeView(
        "sloka-2",
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="chapter-2",
            sloka_id="sloka-2",
        ),
    )
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    result = navigator.next_sloka(current)
    assert result is not None
    assert result.chapter_id == "chapter-2"
    assert result.sloka_id == "sloka-2"
    assert result.purana_id == "purana-1"

def test_next_sloka_falls_back_to_current_chapter_id():
    navigator, repository = make_navigator()
    repository.slokas["sloka-2"] = FakeView(
        "sloka-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id="sloka-2",
        ),
    )
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-7",
        sloka_id="sloka-1",
    )
    result = navigator.next_sloka(current)
    assert result is not None
    assert result.chapter_id == "chapter-7"
    assert result.sloka_id == "sloka-2"

def test_next_sloka_rejects_missing_chapter_context():
    navigator, repository = make_navigator()
    repository.slokas["sloka-2"] = FakeView(
        "sloka-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id="sloka-2",
        ),
    )
    current = ReaderPosition(
        purana_id="purana-1",
        chapter_id=None,
        sloka_id="sloka-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="Unable to determine chapter_id for sloka navigation.",
    ):
        navigator.next_sloka(current)

# =============================================================
# Word Tests
# =============================================================
def test_next_word_preserves_structural_context():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )
    result = navigator.next_word(current)
    assert result is not None
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert result.word_id == "word-2"
    assert repository.calls[-1] == ("next_word", "word-1")

def test_previous_word_preserves_structural_context():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )
    result = navigator.previous_word(current)
    assert result is not None
    assert result.purana_id == "purana-1"
    assert result.chapter_id == "chapter-1"
    assert result.sloka_id == "sloka-1"
    assert result.word_id == "word-1"
    assert repository.calls[-1] == ("previous_word", "word-2")

def test_first_word_has_no_previous():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )
    assert navigator.previous_word(current) is None

def test_last_word_has_no_next():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-3",
    )
    assert navigator.next_word(current) is None

def test_next_word_requires_word_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="ReaderPosition does not contain a word_id.",
    ):
        navigator.next_word(current)
    assert repository.calls == []

def test_previous_word_requires_word_id():
    navigator, repository = make_navigator()
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="ReaderPosition does not contain a word_id.",
    ):
        navigator.previous_word(current)
    assert repository.calls == []

def test_next_word_uses_target_view_structural_context():
    navigator, repository = make_navigator()
    repository.words["word-2"] = FakeView(
        "word-2",
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-2",
            sloka_id="sloka-9",
            word_id="word-2",
        ),
    )
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )
    result = navigator.next_word(current)
    assert result is not None
    assert result.chapter_id == "chapter-2"
    assert result.sloka_id == "sloka-9"
    assert result.word_id == "word-2"

def test_next_word_falls_back_to_current_chapter_id():
    navigator, repository = make_navigator()
    repository.words["word-2"] = FakeView(
        "word-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id="sloka-2",
            word_id="word-2",
        ),
    )
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-7",
        sloka_id="sloka-1",
        word_id="word-1",
    )
    result = navigator.next_word(current)
    assert result is not None
    assert result.chapter_id == "chapter-7"
    assert result.sloka_id == "sloka-2"
    assert result.word_id == "word-2"

def test_next_word_falls_back_to_current_sloka_id():
    navigator, repository = make_navigator()
    repository.words["word-2"] = FakeView(
        "word-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id="chapter-8",
            sloka_id=None,
            word_id="word-2",
        ),
    )
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-7",
        sloka_id="sloka-7",
        word_id="word-1",
    )
    result = navigator.next_word(current)
    assert result is not None
    assert result.chapter_id == "chapter-8"
    assert result.sloka_id == "sloka-7"
    assert result.word_id == "word-2"

def test_next_word_falls_back_to_current_structural_context():
    navigator, repository = make_navigator()
    repository.words["word-2"] = FakeView(
        "word-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id=None,
            word_id="word-2",
        ),
    )
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-7",
        sloka_id="sloka-7",
        word_id="word-1",
    )
    result = navigator.next_word(current)
    assert result is not None
    assert result.chapter_id == "chapter-7"
    assert result.sloka_id == "sloka-7"
    assert result.word_id == "word-2"

def test_next_word_rejects_missing_chapter_context():
    navigator, repository = make_navigator()
    repository.words["word-2"] = FakeView(
        "word-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id="sloka-2",
            word_id="word-2",
        ),
    )
    current = ReaderPosition(
        purana_id="purana-1",
        chapter_id=None,
        sloka_id="sloka-1",
        word_id="word-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="Unable to determine chapter_id for word navigation.",
    ):
        navigator.next_word(current)

def test_next_word_rejects_missing_sloka_context():
    navigator, repository = make_navigator()
    repository.words["word-2"] = FakeView(
        "word-2",
        ReaderPosition(
            purana_id="purana-1",
            chapter_id="chapter-2",
            sloka_id=None,
            word_id="word-2",
        ),
    )
    current = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id=None,
        word_id="word-1",
    )
    with __import__("pytest").raises(
        ValueError,
        match="Unable to determine sloka_id for word navigation.",
    ):
        navigator.next_word(current)

# =============================================================
# Factory Injection
# =============================================================
def test_navigator_uses_injected_position_factory_for_chapter():
    factory = SpyPositionFactory()
    navigator, _ = make_navigator(factory)
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    result = navigator.next_chapter(current)
    assert result.chapter_id == "chapter-2"
    assert factory.calls == [
        ("chapter", "purana-1", "chapter-2")
    ]

def test_navigator_uses_injected_position_factory_for_sloka():
    factory = SpyPositionFactory()
    navigator, _ = make_navigator(factory)
    current = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    result = navigator.next_sloka(current)
    assert result.sloka_id == "sloka-2"
    assert factory.calls == [
        ("sloka", "purana-1", "chapter-1", "sloka-2")
    ]

def test_navigator_uses_injected_position_factory_for_word():
    factory = SpyPositionFactory()
    navigator, _ = make_navigator(factory)
    current = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )
    result = navigator.next_word(current)
    assert result.word_id == "word-2"
    assert factory.calls == [
        ("word", "purana-1", "chapter-1", "sloka-1", "word-2")
    ]

def test_navigator_uses_default_position_factory():
    navigator, repository = make_default_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    result = navigator.next_chapter(current)
    assert result is not None
    assert result == ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )
    assert repository.calls[-1] == (
        "next_chapter",
        "chapter-1",
    )

# =============================================================
# Immutability / No-Index Contract
# =============================================================
def test_navigation_returns_new_immutable_position():
    navigator, _ = make_navigator()
    current = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )
    result = navigator.next_chapter(current)
    assert result is not None
    assert result is not current
    try:
        result.chapter_id = "chapter-x"
    except Exception:
        pass
    else:
        raise AssertionError(
            "ReaderPosition must be immutable."
        )

def test_navigator_does_not_require_indices():
    """
    The Reader navigation contract is identifier-based.
    This test intentionally constructs a position without any
    chapter/sloka/word index attributes.
    """
    navigator, _ = make_navigator()
    position = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )
    assert not hasattr(position, "chapter_index")
    assert not hasattr(position, "sloka_index")
    assert not hasattr(position, "word_index")
    result = navigator.next_sloka(position)
    assert result.sloka_id == "sloka-2"

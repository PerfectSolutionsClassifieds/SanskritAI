
from __future__ import annotations

"""
SanskritAI
==========

ReaderPosition Unit Tests

Locks down the observable contract of the immutable ReaderPosition
value object.

Coverage
--------
* construction
* hierarchical validation
* level detection
* level predicates
* canonical_id
* identifier compatibility alias
* parent-position projections
* serialization
* string representation
* immutability
* equality
* hashing

Version
-------
v1.0.0
"""

import pytest

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


# =============================================================
# Construction
# =============================================================


def test_purana_level_position():
    position = ReaderPosition(
        purana_id="purana-1",
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id is None
    assert position.sloka_id is None
    assert position.word_id is None


def test_chapter_level_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert position.level == "chapter"
    assert position.chapter_id == "chapter-1"


def test_sloka_level_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    assert position.level == "sloka"
    assert position.sloka_id == "sloka-1"


def test_word_level_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position.level == "word"
    assert position.word_id == "word-1"


# =============================================================
# Validation
# =============================================================


def test_empty_purana_id_is_rejected():
    with pytest.raises(ValueError):
        ReaderPosition(
            purana_id="",
        )


def test_missing_purana_id_is_rejected():
    with pytest.raises(ValueError):
        ReaderPosition(
            purana_id=None,
        )


def test_sloka_requires_chapter():
    with pytest.raises(ValueError):
        ReaderPosition(
            purana_id="purana-1",
            sloka_id="sloka-1",
        )


def test_word_requires_sloka():
    with pytest.raises(ValueError):
        ReaderPosition(
            purana_id="purana-1",
            chapter_id="chapter-1",
            word_id="word-1",
        )


def test_word_requires_complete_hierarchy():
    with pytest.raises(ValueError):
        ReaderPosition(
            purana_id="purana-1",
            word_id="word-1",
        )


# =============================================================
# Level
# =============================================================


def test_level_is_purana():
    position = ReaderPosition(
        purana_id="purana-1",
    )

    assert position.level == "purana"


def test_level_is_chapter():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert position.level == "chapter"


def test_level_is_sloka():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    assert position.level == "sloka"


def test_level_is_word():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position.level == "word"


# =============================================================
# Level Predicates
# =============================================================


def test_purana_level_predicates():
    position = ReaderPosition(
        purana_id="purana-1",
    )

    assert position.is_purana is True
    assert position.is_chapter is False
    assert position.is_sloka is False
    assert position.is_word is False


def test_chapter_level_predicates():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert position.is_purana is False
    assert position.is_chapter is True
    assert position.is_sloka is False
    assert position.is_word is False


def test_sloka_level_predicates():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    assert position.is_purana is False
    assert position.is_chapter is False
    assert position.is_sloka is True
    assert position.is_word is False


def test_word_level_predicates():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position.is_purana is False
    assert position.is_chapter is False
    assert position.is_sloka is False
    assert position.is_word is True


# =============================================================
# Canonical Identity
# =============================================================


def test_canonical_id_at_purana_level():
    position = ReaderPosition(
        purana_id="purana-1",
    )

    assert position.canonical_id == "purana-1"


def test_canonical_id_at_chapter_level():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert position.canonical_id == "chapter-1"


def test_canonical_id_at_sloka_level():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    assert position.canonical_id == "sloka-1"


def test_canonical_id_at_word_level():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position.canonical_id == "word-1"


# =============================================================
# Identifier Alias
# =============================================================


def test_identifier_matches_canonical_id():
    positions = (
        ReaderPosition(
            purana_id="purana-1",
        ),
        ReaderPosition(
            purana_id="purana-1",
            chapter_id="chapter-1",
        ),
        ReaderPosition(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        ),
        ReaderPosition(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        ),
    )

    for position in positions:
        assert position.identifier == position.canonical_id


# =============================================================
# Parent Positions
# =============================================================


def test_chapter_position_from_chapter_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    parent = position.chapter_position

    assert parent == position
    assert parent.level == "chapter"


def test_chapter_position_from_sloka_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    parent = position.chapter_position

    assert parent == ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )


def test_chapter_position_from_word_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    parent = position.chapter_position

    assert parent == ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )


def test_chapter_position_requires_chapter():
    position = ReaderPosition(
        purana_id="purana-1",
    )

    with pytest.raises(ValueError):
        _ = position.chapter_position


def test_sloka_position_from_sloka_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    sloka = position.sloka_position

    assert sloka == position


def test_sloka_position_from_word_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    sloka = position.sloka_position

    assert sloka == ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )


def test_sloka_position_requires_sloka():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    with pytest.raises(ValueError):
        _ = position.sloka_position


def test_word_position_from_word_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    word = position.word_position

    assert word == position


def test_word_position_requires_word():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    with pytest.raises(ValueError):
        _ = position.word_position


# =============================================================
# Parent Position Immutability
# =============================================================


def test_parent_position_is_a_new_immutable_reader_position():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    chapter = position.chapter_position

    assert chapter is not position

    with pytest.raises(Exception):
        chapter.chapter_id = "chapter-x"


# =============================================================
# Serialization
# =============================================================


def test_to_dict_contains_canonical_fields():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    data = position.to_dict()

    assert data == {
        "purana_id": "purana-1",
        "chapter_id": "chapter-1",
        "sloka_id": "sloka-1",
        "word_id": "word-1",
        "level": "word",
        "canonical_id": "word-1",
        "identifier": "word-1",
    }


def test_to_dict_at_chapter_level():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    data = position.to_dict()

    assert data["purana_id"] == "purana-1"
    assert data["chapter_id"] == "chapter-1"
    assert data["sloka_id"] is None
    assert data["word_id"] is None
    assert data["level"] == "chapter"
    assert data["canonical_id"] == "chapter-1"
    assert data["identifier"] == "chapter-1"


# =============================================================
# String Representation
# =============================================================


def test_string_representation_returns_canonical_id():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert str(position) == "word-1"


def test_string_representation_at_chapter_level():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert str(position) == "chapter-1"


# =============================================================
# Representation
# =============================================================


def test_repr_contains_all_identifiers():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    representation = repr(position)

    assert "ReaderPosition" in representation
    assert "purana-1" in representation
    assert "chapter-1" in representation
    assert "sloka-1" in representation
    assert "word-1" in representation


# =============================================================
# Immutability
# =============================================================


def test_reader_position_is_immutable():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    with pytest.raises(Exception):
        position.chapter_id = "chapter-2"


def test_reader_position_cannot_change_purana_id():
    position = ReaderPosition(
        purana_id="purana-1",
    )

    with pytest.raises(Exception):
        position.purana_id = "purana-2"


# =============================================================
# Equality
# =============================================================


def test_equal_positions_are_equal():
    position_a = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    position_b = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position_a == position_b


def test_different_positions_are_not_equal():
    position_a = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    position_b = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )

    assert position_a != position_b


# =============================================================
# Hashing
# =============================================================


def test_reader_position_is_hashable():
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert hash(position) == hash(position)


def test_equal_positions_have_equal_hashes():
    position_a = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    position_b = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert hash(position_a) == hash(position_b)

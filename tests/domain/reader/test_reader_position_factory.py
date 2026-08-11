
from __future__ import annotations

"""
SanskritAI
==========

ReaderPositionFactory Tests

Verifies:

* purana position construction
* chapter position construction
* sloka position construction
* word position construction
* identifier normalization
* None rejection
* empty identifier rejection
* whitespace rejection
* canonical ReaderPosition hierarchy
* ReaderPosition immutability
* ReaderPositionFactory immutability
* keyword-only factory API
* factory returns ReaderPosition instances

ReaderPositionFactory is the centralized constructor for
canonical immutable ReaderPosition objects.

Version
-------
v1.0.0
"""

import pytest

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_position_factory import (
    ReaderPositionFactory,
)


# =============================================================
# Purāṇa
# =============================================================


def test_purana_constructs_reader_position():
    position = ReaderPositionFactory.purana(
        purana_id="purana-1",
    )

    assert isinstance(
        position,
        ReaderPosition,
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id is None
    assert position.sloka_id is None
    assert position.word_id is None

    assert position.level == "purana"
    assert position.canonical_id == "purana-1"
    assert position.identifier == "purana-1"


def test_purana_normalizes_identifier():
    position = ReaderPositionFactory.purana(
        purana_id="  purana-1  ",
    )

    assert position.purana_id == "purana-1"


def test_purana_rejects_none():
    with pytest.raises(ValueError):
        ReaderPositionFactory.purana(
            purana_id=None,
        )


def test_purana_rejects_empty_string():
    with pytest.raises(ValueError):
        ReaderPositionFactory.purana(
            purana_id="",
        )


def test_purana_rejects_whitespace_only_identifier():
    with pytest.raises(ValueError):
        ReaderPositionFactory.purana(
            purana_id="   ",
        )


# =============================================================
# Chapter
# =============================================================


def test_chapter_constructs_reader_position():
    position = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    assert isinstance(
        position,
        ReaderPosition,
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id == "chapter-1"
    assert position.sloka_id is None
    assert position.word_id is None

    assert position.level == "chapter"
    assert position.canonical_id == "chapter-1"
    assert position.identifier == "chapter-1"


def test_chapter_normalizes_identifiers():
    position = ReaderPositionFactory.chapter(
        purana_id="  purana-1  ",
        chapter_id="  chapter-1  ",
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id == "chapter-1"


def test_chapter_rejects_none_purana_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.chapter(
            purana_id=None,
            chapter_id="chapter-1",
        )


def test_chapter_rejects_none_chapter_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.chapter(
            purana_id="purana-1",
            chapter_id=None,
        )


def test_chapter_rejects_empty_purana_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.chapter(
            purana_id="",
            chapter_id="chapter-1",
        )


def test_chapter_rejects_empty_chapter_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.chapter(
            purana_id="purana-1",
            chapter_id="",
        )


def test_chapter_rejects_whitespace_purana_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.chapter(
            purana_id="   ",
            chapter_id="chapter-1",
        )


def test_chapter_rejects_whitespace_chapter_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.chapter(
            purana_id="purana-1",
            chapter_id="   ",
        )


# =============================================================
# Śloka
# =============================================================


def test_sloka_constructs_reader_position():
    position = ReaderPositionFactory.sloka(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
    )

    assert isinstance(
        position,
        ReaderPosition,
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id == "chapter-1"
    assert position.sloka_id == "sloka-1"
    assert position.word_id is None

    assert position.level == "sloka"
    assert position.canonical_id == "sloka-1"
    assert position.identifier == "sloka-1"


def test_sloka_normalizes_identifiers():
    position = ReaderPositionFactory.sloka(
        purana_id="  purana-1 ",
        chapter_id=" chapter-1 ",
        sloka_id=" sloka-1 ",
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id == "chapter-1"
    assert position.sloka_id == "sloka-1"


def test_sloka_rejects_none_purana_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id=None,
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        )


def test_sloka_rejects_none_chapter_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id="sloka-1",
        )


def test_sloka_rejects_none_sloka_id():
    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id=None,
        )


def test_sloka_rejects_empty_identifiers():
    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="",
            sloka_id="sloka-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="",
        )


def test_sloka_rejects_whitespace_identifiers():
    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="   ",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="   ",
            sloka_id="sloka-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="   ",
        )


# =============================================================
# Word
# =============================================================


def test_word_constructs_reader_position():
    position = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert isinstance(
        position,
        ReaderPosition,
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id == "chapter-1"
    assert position.sloka_id == "sloka-1"
    assert position.word_id == "word-1"

    assert position.level == "word"
    assert position.canonical_id == "word-1"
    assert position.identifier == "word-1"


def test_word_normalizes_identifiers():
    position = ReaderPositionFactory.word(
        purana_id=" purana-1 ",
        chapter_id=" chapter-1 ",
        sloka_id=" sloka-1 ",
        word_id=" word-1 ",
    )

    assert position.purana_id == "purana-1"
    assert position.chapter_id == "chapter-1"
    assert position.sloka_id == "sloka-1"
    assert position.word_id == "word-1"


def test_word_rejects_none_identifiers():
    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id=None,
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id=None,
            sloka_id="sloka-1",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id=None,
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id=None,
        )


def test_word_rejects_empty_identifiers():
    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="",
            sloka_id="sloka-1",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="",
        )


def test_word_rejects_whitespace_identifiers():
    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="   ",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="   ",
            sloka_id="sloka-1",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="   ",
            word_id="word-1",
        )

    with pytest.raises(ValueError):
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="   ",
        )


# =============================================================
# Hierarchy Contract
# =============================================================


def test_factory_preserves_complete_hierarchy():
    position = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position.level == "word"

    assert position.chapter_position == (
        ReaderPositionFactory.chapter(
            purana_id="purana-1",
            chapter_id="chapter-1",
        )
    )

    assert position.sloka_position == (
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        )
    )

    assert position.word_position == position


def test_factory_positions_have_no_index_attributes():
    positions = (
        ReaderPositionFactory.purana(
            purana_id="purana-1",
        ),
        ReaderPositionFactory.chapter(
            purana_id="purana-1",
            chapter_id="chapter-1",
        ),
        ReaderPositionFactory.sloka(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
        ),
        ReaderPositionFactory.word(
            purana_id="purana-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        ),
    )

    for position in positions:
        assert not hasattr(
            position,
            "purana_index",
        )

        assert not hasattr(
            position,
            "chapter_index",
        )

        assert not hasattr(
            position,
            "sloka_index",
        )

        assert not hasattr(
            position,
            "word_index",
        )


# =============================================================
# Immutability
# =============================================================


def test_factory_returns_immutable_positions():
    position = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    with pytest.raises(Exception):
        position.word_id = "word-2"


def test_factory_itself_is_immutable():
    factory = ReaderPositionFactory()

    with pytest.raises(Exception):
        factory.some_attribute = "changed"


# =============================================================
# Keyword-Only API
# =============================================================


def test_purana_factory_requires_keyword_argument():
    with pytest.raises(TypeError):
        ReaderPositionFactory.purana(
            "purana-1",
        )


def test_chapter_factory_requires_keyword_arguments():
    with pytest.raises(TypeError):
        ReaderPositionFactory.chapter(
            "purana-1",
            "chapter-1",
        )


def test_sloka_factory_requires_keyword_arguments():
    with pytest.raises(TypeError):
        ReaderPositionFactory.sloka(
            "purana-1",
            "chapter-1",
            "sloka-1",
        )


def test_word_factory_requires_keyword_arguments():
    with pytest.raises(TypeError):
        ReaderPositionFactory.word(
            "purana-1",
            "chapter-1",
            "sloka-1",
            "word-1",
        )


# =============================================================
# Type Conversion
# =============================================================


def test_factory_converts_identifier_values_to_strings():
    position = ReaderPositionFactory.word(
        purana_id=123,
        chapter_id=456,
        sloka_id=789,
        word_id=101112,
    )

    assert position.purana_id == "123"
    assert position.chapter_id == "456"
    assert position.sloka_id == "789"
    assert position.word_id == "101112"


# =============================================================
# Equality
# =============================================================


def test_factory_produces_equal_positions_for_equal_identifiers():
    position_a = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    position_b = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position_a == position_b


def test_factory_produces_distinct_positions_for_distinct_identifiers():
    position_a = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-1",
    )

    position_b = ReaderPositionFactory.chapter(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )

    assert position_a != position_b


# =============================================================
# Serialization
# =============================================================


def test_factory_position_serializes_correctly():
    position = ReaderPositionFactory.word(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )

    assert position.to_dict() == {
        "purana_id": "purana-1",
        "chapter_id": "chapter-1",
        "sloka_id": "sloka-1",
        "word_id": "word-1",
        "level": "word",
        "canonical_id": "word-1",
        "identifier": "word-1",
    }

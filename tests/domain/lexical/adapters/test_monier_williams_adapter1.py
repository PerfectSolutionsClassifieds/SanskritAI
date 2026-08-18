from __future__ import annotations

import pytest

from SanskritAI.domain.lexical.adapters import (
    InMemoryMonierWilliamsAdapter,
    MonierWilliamsRecord,
)


def make_adapter() -> InMemoryMonierWilliamsAdapter:
    return InMemoryMonierWilliamsAdapter(
        records=(
            MonierWilliamsRecord(
                headword="राम",
                transliteration="rāma",
                definition="pleasing, beautiful; Rāma",
                grammatical_label="noun",
            ),
            MonierWilliamsRecord(
                headword="गम्",
                transliteration="gam",
                definition="to go",
                grammatical_label="verb",
            ),
        )
    )


def test_adapter_source():
    adapter = make_adapter()

    assert adapter.source == "monier-williams"


def test_adapter_count():
    adapter = make_adapter()

    assert adapter.count == 2


def test_lookup_returns_exact_headword():
    adapter = make_adapter()

    result = adapter.lookup("राम")

    assert len(result) == 1
    assert result[0].headword == "राम"


def test_lookup_normalizes_whitespace():
    adapter = make_adapter()

    result = adapter.lookup("  राम  ")

    assert len(result) == 1
    assert result[0].headword == "राम"


def test_lookup_unknown_headword_returns_empty():
    adapter = make_adapter()

    assert adapter.lookup("कृष्ण") == ()


def test_search_matches_headword():
    adapter = make_adapter()

    result = adapter.search("राम")

    assert len(result) == 1
    assert result[0].headword == "राम"


def test_search_matches_definition():
    adapter = make_adapter()

    result = adapter.search("go")

    assert len(result) == 1
    assert result[0].headword == "गम्"


def test_search_empty_query_returns_empty():
    adapter = make_adapter()

    assert adapter.search("") == ()


def test_all_records_returns_all_records():
    adapter = make_adapter()

    records = adapter.all_records()

    assert len(records) == 2
    assert isinstance(records, tuple)


def test_records_are_normalized():
    adapter = InMemoryMonierWilliamsAdapter(
        records=(
            MonierWilliamsRecord(
                headword="  राम  ",
                transliteration=" rāma ",
                definition=" pleasing ",
                grammatical_label=" noun ",
            ),
        )
    )

    record = adapter.all_records()[0]

    assert record.headword == "राम"
    assert record.transliteration == "rāma"
    assert record.definition == "pleasing"
    assert record.grammatical_label == "noun"


def test_normalize_headword_requires_string():
    with pytest.raises(TypeError):
        MonierWilliamsRecord(
            headword="राम",
        )

        InMemoryMonierWilliamsAdapter().normalize_headword(
            None,
        )

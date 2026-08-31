
from types import SimpleNamespace

from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
)


def make_source(source_id: str):
    return SimpleNamespace(source_id=source_id)


def make_sense(name: str):
    return SimpleNamespace(name=name)


def test_index_starts_empty():
    index = SourceIndex()

    assert len(index) == 0
    assert index.source_count == 0
    assert index.summary() == {"sources": 0}


def test_add_registers_sense_under_source_id():
    index = SourceIndex()

    source = make_source("MW")
    sense = make_sense("sense-1")

    index.add(source, sense)

    assert len(index) == 1
    assert "MW" in index
    assert index.lookup("MW") == (sense,)


def test_multiple_senses_share_same_source_bucket():
    index = SourceIndex()

    source = make_source("MW")

    first = make_sense("sense-1")
    second = make_sense("sense-2")

    index.add(source, first)
    index.add(source, second)

    assert index.source_count == 1
    assert index.lookup("MW") == (
        first,
        second,
    )


def test_different_sources_create_different_buckets():
    index = SourceIndex()

    mw = make_source("MW")
    apte = make_source("APTE")

    first = make_sense("sense-1")
    second = make_sense("sense-2")

    index.add(mw, first)
    index.add(apte, second)

    assert index.source_count == 2
    assert index.lookup("MW") == (first,)
    assert index.lookup("APTE") == (second,)


def test_lookup_unknown_source_returns_empty_tuple():
    index = SourceIndex()

    assert index.lookup("UNKNOWN") == ()


def test_clear_removes_all_sources():
    index = SourceIndex()

    index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )

    index.clear()

    assert len(index) == 0
    assert index.source_count == 0
    assert index.lookup("MW") == ()


def test_summary_reports_source_count():
    index = SourceIndex()

    index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )
    index.add(
        make_source("APTE"),
        make_sense("sense-2"),
    )

    assert index.summary() == {
        "sources": 2,
    }


def test_contains_checks_source_id():
    index = SourceIndex()

    index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )

    assert "MW" in index
    assert "APTE" not in index


def test_iteration_returns_sorted_source_ids():
    index = SourceIndex()

    index.add(
        make_source("VCP"),
        make_sense("sense-1"),
    )
    index.add(
        make_source("MW"),
        make_sense("sense-2"),
    )
    index.add(
        make_source("APTE"),
        make_sense("sense-3"),
    )

    assert tuple(index) == (
        "APTE",
        "MW",
        "VCP",
    )


def test_string_representation_contains_source_count():
    index = SourceIndex()

    index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )

    assert str(index) == "SourceIndex(1 sources)"
    

from types import SimpleNamespace

from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)


def make_context(identifier: str):
    return SimpleNamespace(identifier=identifier)


def make_sense(name: str):
    return SimpleNamespace(name=name)


def test_index_starts_empty():
    index = ContextIndex()

    assert len(index) == 0
    assert index.context_count == 0
    assert index.summary() == {"contexts": 0}


def test_add_registers_sense_under_context_identifier():
    index = ContextIndex()

    context = make_context("chapter-1")
    sense = make_sense("sense-1")

    index.add(context, sense)

    assert len(index) == 1
    assert context.identifier in index
    assert index.lookup("chapter-1") == (sense,)


def test_multiple_senses_share_same_context_bucket():
    index = ContextIndex()

    context = make_context("chapter-1")

    first = make_sense("sense-1")
    second = make_sense("sense-2")

    index.add(context, first)
    index.add(context, second)

    assert index.context_count == 1
    assert index.lookup("chapter-1") == (
        first,
        second,
    )


def test_different_contexts_create_different_buckets():
    index = ContextIndex()

    first_context = make_context("chapter-1")
    second_context = make_context("chapter-2")

    first = make_sense("sense-1")
    second = make_sense("sense-2")

    index.add(first_context, first)
    index.add(second_context, second)

    assert index.context_count == 2
    assert index.lookup("chapter-1") == (first,)
    assert index.lookup("chapter-2") == (second,)


def test_lookup_unknown_context_returns_empty_tuple():
    index = ContextIndex()

    assert index.lookup("unknown") == ()


def test_clear_removes_all_contexts():
    index = ContextIndex()

    index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )

    index.clear()

    assert len(index) == 0
    assert index.context_count == 0
    assert index.lookup("chapter-1") == ()


def test_summary_reports_context_count():
    index = ContextIndex()

    index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )
    index.add(
        make_context("chapter-2"),
        make_sense("sense-2"),
    )

    assert index.summary() == {
        "contexts": 2,
    }


def test_contains_checks_context_identifier():
    index = ContextIndex()

    index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )

    assert "chapter-1" in index
    assert "chapter-2" not in index


def test_iteration_returns_sorted_context_identifiers():
    index = ContextIndex()

    index.add(
        make_context("chapter-2"),
        make_sense("sense-2"),
    )
    index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )

    assert tuple(index) == (
        "chapter-1",
        "chapter-2",
    )


def test_string_representation_contains_context_count():
    index = ContextIndex()

    index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )

    assert str(index) == "ContextIndex(1 contexts)"

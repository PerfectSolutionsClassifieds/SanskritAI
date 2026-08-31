
from types import SimpleNamespace

from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)


def make_entry(headword: str):
    return SimpleNamespace(
        headword=headword,
    )


def test_index_starts_empty():
    index = HeadwordIndex()

    assert len(index) == 0
    assert index.headwords == ()
    assert index.all_entries() == ()


def test_add_indexes_entry_by_headword():
    index = HeadwordIndex()
    entry = make_entry("राम")

    index.add(entry)

    assert len(index) == 1
    assert index.lookup("राम") is entry
    assert "राम" in index


def test_add_strips_headword_before_indexing():
    index = HeadwordIndex()
    entry = make_entry("  राम  ")

    index.add(entry)

    assert index.lookup("राम") is entry
    assert "राम" in index


def test_add_ignores_empty_headword():
    index = HeadwordIndex()
    entry = make_entry("   ")

    index.add(entry)

    assert len(index) == 0
    assert index.lookup("") is None


def test_add_preserves_first_entry_for_duplicate_headword():
    index = HeadwordIndex()

    first = make_entry("राम")
    second = make_entry("राम")

    index.add(first)
    index.add(second)

    assert len(index) == 1
    assert index.lookup("राम") is first


def test_build_replaces_existing_index():
    index = HeadwordIndex()

    old_entry = make_entry("पुरातन")
    new_entries = (
        make_entry("राम"),
        make_entry("हरि"),
    )

    index.add(old_entry)
    index.build(new_entries)

    assert len(index) == 2
    assert index.lookup("पुरातन") is None
    assert index.lookup("राम") is new_entries[0]
    assert index.lookup("हरि") is new_entries[1]


def test_clear_removes_all_entries():
    index = HeadwordIndex()

    index.build(
        (
            make_entry("राम"),
            make_entry("हरि"),
        )
    )

    index.clear()

    assert len(index) == 0
    assert index.headwords == ()
    assert index.all_entries() == ()


def test_lookup_returns_none_for_unknown_headword():
    index = HeadwordIndex()

    index.add(make_entry("राम"))

    assert index.lookup("हरि") is None


def test_prefix_search_returns_matching_entries():
    index = HeadwordIndex()

    ram = make_entry("राम")
    rama = make_entry("रामायण")
    hari = make_entry("हरि")

    index.build((hari, rama, ram))

    result = index.prefix_search("राम")

    assert result == (ram, rama)


def test_prefix_search_returns_sorted_results():
    index = HeadwordIndex()

    z = make_entry("रामेश")
    a = make_entry("राम")
    m = make_entry("रामकथा")

    index.build((z, a, m))

    result = index.prefix_search("राम")

    assert tuple(entry.headword for entry in result) == (
        "राम",
        "रामकथा",
        "रामेश",
    )


def test_prefix_search_strips_prefix():
    index = HeadwordIndex()

    entry = make_entry("रामायण")
    index.add(entry)

    assert index.prefix_search("  राम") == (entry,)


def test_empty_prefix_search_returns_empty_tuple():
    index = HeadwordIndex()

    index.add(make_entry("राम"))

    assert index.prefix_search("") == ()
    assert index.prefix_search("   ") == ()


def test_all_entries_are_sorted_by_headword():
    index = HeadwordIndex()

    ram = make_entry("राम")
    hari = make_entry("हरि")
    gita = make_entry("गीता")

    index.build((ram, hari, gita))

    result = index.all_entries()

    assert tuple(entry.headword for entry in result) == tuple(
        sorted(("राम", "हरि", "गीता"))
    )


def test_headwords_are_sorted():
    index = HeadwordIndex()

    index.build(
        (
            make_entry("राम"),
            make_entry("हरि"),
            make_entry("गीता"),
        )
    )

    assert index.headwords == tuple(
        sorted(("राम", "हरि", "गीता"))
    )


def test_summary_reports_indexed_entries_and_headwords():
    index = HeadwordIndex()

    index.build(
        (
            make_entry("राम"),
            make_entry("हरि"),
        )
    )

    assert index.summary() == {
        "indexed_entries": 2,
        "headwords": 2,
    }


def test_iteration_returns_sorted_entries():
    index = HeadwordIndex()

    ram = make_entry("राम")
    hari = make_entry("हरि")

    index.build((ram, hari))

    assert tuple(index) == index.all_entries()


def test_contains_uses_exact_headword():
    index = HeadwordIndex()

    index.add(make_entry("राम"))

    assert "राम" in index
    assert "रामायण" not in index


def test_string_representation_contains_count():
    index = HeadwordIndex()

    index.build(
        (
            make_entry("राम"),
            make_entry("हरि"),
        )
    )

    assert str(index) == "HeadwordIndex(2 indexed entries)"

    

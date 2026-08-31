
from types import SimpleNamespace

from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)


def make_lemma(
    lemma_id: str,
    text: str,
):
    return SimpleNamespace(
        lemma_id=lemma_id,
        text=text,
    )


def test_index_starts_empty():
    index = LemmaIndex()

    assert len(index) == 0
    assert index.lemma_ids == ()
    assert index.lemma_texts == ()
    assert index.all() == ()


def test_add_indexes_by_id_and_text():
    index = LemmaIndex()
    lemma = make_lemma("LEMMA-1", "राम")

    index.add(lemma)

    assert len(index) == 1
    assert index.lookup("LEMMA-1") is lemma
    assert index.lookup_text("राम") is lemma
    assert "LEMMA-1" in index


def test_add_preserves_first_lemma_for_duplicate_id():
    index = LemmaIndex()

    first = make_lemma("LEMMA-1", "राम")
    second = make_lemma("LEMMA-1", "राघव")

    index.add(first)
    index.add(second)

    assert len(index) == 1
    assert index.lookup("LEMMA-1") is first


def test_add_preserves_first_lemma_for_duplicate_text():
    index = LemmaIndex()

    first = make_lemma("LEMMA-1", "राम")
    second = make_lemma("LEMMA-2", "राम")

    index.add(first)
    index.add(second)

    assert len(index) == 2
    assert index.lookup_text("राम") is first


def test_build_replaces_existing_index():
    index = LemmaIndex()

    index.add(make_lemma("OLD", "पुरातन"))

    entries = (
        make_lemma("L1", "राम"),
        make_lemma("L2", "हरि"),
    )

    index.build(entries)

    assert len(index) == 2
    assert index.lookup("OLD") is None
    assert index.lookup("L1") is entries[0]
    assert index.lookup("L2") is entries[1]


def test_clear_removes_both_indexes():
    index = LemmaIndex()

    index.build(
        (
            make_lemma("L1", "राम"),
            make_lemma("L2", "हरि"),
        )
    )

    index.clear()

    assert len(index) == 0
    assert index.lookup("L1") is None
    assert index.lookup_text("राम") is None


def test_lookup_returns_none_for_unknown_id():
    index = LemmaIndex()

    index.add(make_lemma("L1", "राम"))

    assert index.lookup("UNKNOWN") is None


def test_lookup_text_returns_none_for_unknown_text():
    index = LemmaIndex()

    index.add(make_lemma("L1", "राम"))

    assert index.lookup_text("हरि") is None


def test_all_returns_lemmas_sorted_by_text():
    index = LemmaIndex()

    ram = make_lemma("L1", "राम")
    hari = make_lemma("L2", "हरि")
    gita = make_lemma("L3", "गीता")

    index.build((ram, hari, gita))

    result = index.all()

    assert tuple(item.text for item in result) == tuple(
        sorted(("राम", "हरि", "गीता"))
    )


def test_lemma_ids_are_sorted():
    index = LemmaIndex()

    index.build(
        (
            make_lemma("L3", "गीता"),
            make_lemma("L1", "राम"),
            make_lemma("L2", "हरि"),
        )
    )

    assert index.lemma_ids == ("L1", "L2", "L3")


def test_lemma_texts_are_sorted():
    index = LemmaIndex()

    index.build(
        (
            make_lemma("L1", "राम"),
            make_lemma("L2", "हरि"),
            make_lemma("L3", "गीता"),
        )
    )

    assert index.lemma_texts == tuple(
        sorted(("राम", "हरि", "गीता"))
    )


def test_summary_reports_counts():
    index = LemmaIndex()

    index.build(
        (
            make_lemma("L1", "राम"),
            make_lemma("L2", "हरि"),
        )
    )

    assert index.summary() == {
        "lemmas": 2,
        "lemma_ids": 2,
    }


def test_iteration_returns_all_sorted_lemmas():
    index = LemmaIndex()

    index.build(
        (
            make_lemma("L1", "राम"),
            make_lemma("L2", "हरि"),
        )
    )

    assert tuple(index) == index.all()


def test_contains_checks_lemma_id():
    index = LemmaIndex()

    index.add(make_lemma("L1", "राम"))

    assert "L1" in index
    assert "L2" not in index


def test_string_representation_contains_count():
    index = LemmaIndex()

    index.build(
        (
            make_lemma("L1", "राम"),
            make_lemma("L2", "हरि"),
        )
    )

    assert str(index) == "LemmaIndex(2 indexed lemmas)"

    

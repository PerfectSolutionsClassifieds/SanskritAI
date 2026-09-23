
from __future__ import annotations

from types import SimpleNamespace

from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)
from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)
from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)
from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
)
from SanskritAI.acquisition.knowledge.lookup.lexical_lookup_engine import (
    LexicalLookupEngine,
)


# =========================================================
# Helpers
# =========================================================


def make_entry(headword: str):
    """Create a lightweight entry compatible with HeadwordIndex."""
    return SimpleNamespace(
        headword=headword,
    )


def make_lemma(
    lemma_id: str,
    text: str,
):
    """Create a lightweight lemma compatible with LemmaIndex."""
    return SimpleNamespace(
        lemma_id=lemma_id,
        text=text,
    )


def make_context(identifier: str):
    """Create a lightweight context compatible with ContextIndex."""
    return SimpleNamespace(
        identifier=identifier,
    )


def make_source(source_id: str):
    """Create a lightweight source compatible with SourceIndex."""
    return SimpleNamespace(
        source_id=source_id,
    )


def make_sense(name: str):
    """Create a lightweight sense object."""
    return SimpleNamespace(
        name=name,
    )


def make_engine() -> LexicalLookupEngine:
    """Create a fully initialized LexicalLookupEngine."""
    return LexicalLookupEngine(
        headword_index=HeadwordIndex(),
        lemma_index=LemmaIndex(),
        context_index=ContextIndex(),
        source_index=SourceIndex(),
    )


# =========================================================
# Construction
# =========================================================


def test_engine_can_be_constructed():
    engine = make_engine()

    assert isinstance(
        engine,
        LexicalLookupEngine,
    )


def test_engine_contains_all_four_indexes():
    engine = make_engine()

    assert isinstance(
        engine.headword_index,
        HeadwordIndex,
    )

    assert isinstance(
        engine.lemma_index,
        LemmaIndex,
    )

    assert isinstance(
        engine.context_index,
        ContextIndex,
    )

    assert isinstance(
        engine.source_index,
        SourceIndex,
    )


# =========================================================
# Headword Lookup
# =========================================================


def test_lookup_headword_returns_matching_entry():
    engine = make_engine()

    entry = make_entry("राम")

    engine.headword_index.add(entry)

    assert (
        engine.lookup_headword("राम")
        is entry
    )


def test_lookup_headword_returns_none_for_unknown_headword():
    engine = make_engine()

    engine.headword_index.add(
        make_entry("राम"),
    )

    assert (
        engine.lookup_headword("हरि")
        is None
    )


def test_lookup_headword_delegates_whitespace_normalization():
    engine = make_engine()

    entry = make_entry("राम")

    engine.headword_index.add(entry)

    assert (
        engine.lookup_headword("  राम  ")
        is entry
    )


# =========================================================
# Prefix Search
# =========================================================


def test_prefix_search_returns_matching_entries():
    engine = make_engine()

    ram = make_entry("राम")
    ramayana = make_entry("रामायण")
    hari = make_entry("हरि")

    engine.headword_index.build(
        (
            hari,
            ramayana,
            ram,
        )
    )

    result = engine.prefix_search("राम")

    assert result == (
        ram,
        ramayana,
    )


def test_prefix_search_returns_empty_tuple_for_unknown_prefix():
    engine = make_engine()

    engine.headword_index.add(
        make_entry("राम"),
    )

    assert (
        engine.prefix_search("हरि")
        == ()
    )


# =========================================================
# Lemma Lookup
# =========================================================


def test_lookup_lemma_returns_matching_lemma():
    engine = make_engine()

    lemma = make_lemma(
        "LEMMA-1",
        "राम",
    )

    engine.lemma_index.add(lemma)

    assert (
        engine.lookup_lemma("LEMMA-1")
        is lemma
    )


def test_lookup_lemma_returns_none_for_unknown_id():
    engine = make_engine()

    engine.lemma_index.add(
        make_lemma(
            "LEMMA-1",
            "राम",
        )
    )

    assert (
        engine.lookup_lemma("UNKNOWN")
        is None
    )


def test_lookup_lemma_text_returns_matching_lemma():
    engine = make_engine()

    lemma = make_lemma(
        "LEMMA-1",
        "राम",
    )

    engine.lemma_index.add(lemma)

    assert (
        engine.lookup_lemma_text("राम")
        is lemma
    )


def test_lookup_lemma_text_returns_none_for_unknown_text():
    engine = make_engine()

    engine.lemma_index.add(
        make_lemma(
            "LEMMA-1",
            "राम",
        )
    )

    assert (
        engine.lookup_lemma_text("हरि")
        is None
    )


def test_lookup_lemma_text_delegates_whitespace_normalization():
    engine = make_engine()

    lemma = make_lemma(
        "LEMMA-1",
        "राम",
    )

    engine.lemma_index.add(lemma)

    assert (
        engine.lookup_lemma_text("  राम  ")
        is lemma
    )


# =========================================================
# Context Lookup
# =========================================================


def test_lookup_context_returns_senses_for_context():
    engine = make_engine()

    context = make_context(
        "ramayana.chapter.1",
    )

    sense = make_sense(
        "sense-1",
    )

    engine.context_index.add(
        context,
        sense,
    )

    assert (
        engine.lookup_context(
            "ramayana.chapter.1",
        )
        == (sense,)
    )


def test_lookup_context_returns_empty_tuple_for_unknown_context():
    engine = make_engine()

    assert (
        engine.lookup_context(
            "unknown",
        )
        == ()
    )


def test_lookup_context_delegates_whitespace_normalization():
    engine = make_engine()

    context = make_context(
        "chapter-1",
    )

    sense = make_sense(
        "sense-1",
    )

    engine.context_index.add(
        context,
        sense,
    )

    assert (
        engine.lookup_context(
            "  chapter-1  ",
        )
        == (sense,)
    )


# =========================================================
# Source Lookup
# =========================================================


def test_lookup_source_returns_senses_for_source():
    engine = make_engine()

    source = make_source(
        "monier-williams",
    )

    sense = make_sense(
        "sense-1",
    )

    engine.source_index.add(
        source,
        sense,
    )

    assert (
        engine.lookup_source(
            "monier-williams",
        )
        == (sense,)
    )


def test_lookup_source_returns_empty_tuple_for_unknown_source():
    engine = make_engine()

    assert (
        engine.lookup_source(
            "unknown",
        )
        == ()
    )


def test_lookup_source_delegates_whitespace_normalization():
    engine = make_engine()

    source = make_source(
        "MW",
    )

    sense = make_sense(
        "sense-1",
    )

    engine.source_index.add(
        source,
        sense,
    )

    assert (
        engine.lookup_source(
            "  MW  ",
        )
        == (sense,)
    )


# =========================================================
# Unified Search
# =========================================================


def test_search_returns_headword_lemma_and_prefix_matches():
    engine = make_engine()

    entry = make_entry("राम")

    lemma = make_lemma(
        "LEMMA-1",
        "राम",
    )

    ramayana = make_entry("रामायण")

    engine.headword_index.add(entry)
    engine.headword_index.add(ramayana)
    engine.lemma_index.add(lemma)

    result = engine.search("राम")

    assert result["headword"] is entry

    assert result["lemma"] is lemma

    assert result["prefix_matches"] == (
        entry,
        ramayana,
    )


def test_search_returns_empty_results_for_unknown_query():
    engine = make_engine()

    result = engine.search("हरि")

    assert result["headword"] is None
    assert result["lemma"] is None
    assert result["prefix_matches"] == ()


def test_search_strips_query_through_index_apis():
    engine = make_engine()

    entry = make_entry("राम")

    lemma = make_lemma(
        "LEMMA-1",
        "राम",
    )

    engine.headword_index.add(entry)
    engine.lemma_index.add(lemma)

    result = engine.search("  राम  ")

    assert result["headword"] is entry
    assert result["lemma"] is lemma
    assert result["prefix_matches"] == (entry,)


# =========================================================
# Multiple Indexed Objects
# =========================================================


def test_engine_can_coordinate_multiple_indexes():
    engine = make_engine()

    ram = make_entry("राम")
    hari = make_entry("हरि")

    ram_lemma = make_lemma(
        "LEMMA-RAM",
        "राम",
    )

    hari_lemma = make_lemma(
        "LEMMA-HARI",
        "हरि",
    )

    ram_context = make_context(
        "ramayana.1.1",
    )

    hari_context = make_context(
        "ramayana.1.2",
    )

    ram_sense = make_sense(
        "ram-sense",
    )

    hari_sense = make_sense(
        "hari-sense",
    )

    ram_source = make_source("MW")
    hari_source = make_source("APTE")

    engine.headword_index.build(
        (
            ram,
            hari,
        )
    )

    engine.lemma_index.build(
        (
            ram_lemma,
            hari_lemma,
        )
    )

    engine.context_index.add(
        ram_context,
        ram_sense,
    )

    engine.context_index.add(
        hari_context,
        hari_sense,
    )

    engine.source_index.add(
        ram_source,
        ram_sense,
    )

    engine.source_index.add(
        hari_source,
        hari_sense,
    )

    assert engine.lookup_headword("राम") is ram
    assert engine.lookup_headword("हरि") is hari

    assert (
        engine.lookup_lemma_text("राम")
        is ram_lemma
    )

    assert (
        engine.lookup_lemma_text("हरि")
        is hari_lemma
    )

    assert (
        engine.lookup_context("ramayana.1.1")
        == (ram_sense,)
    )

    assert (
        engine.lookup_context("ramayana.1.2")
        == (hari_sense,)
    )

    assert (
        engine.lookup_source("MW")
        == (ram_sense,)
    )

    assert (
        engine.lookup_source("APTE")
        == (hari_sense,)
    )


# =========================================================
# Diagnostics
# =========================================================


def test_summary_reports_all_index_counts():
    engine = make_engine()

    engine.headword_index.add(
        make_entry("राम"),
    )

    engine.lemma_index.add(
        make_lemma(
            "LEMMA-1",
            "राम",
        )
    )

    engine.context_index.add(
        make_context("context-1"),
        make_sense("sense-1"),
    )

    engine.source_index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )

    assert engine.summary() == {
        "headwords": 1,
        "lemmas": 1,
        "contexts": 1,
        "sources": 1,
    }


def test_empty_engine_summary_reports_zero_counts():
    engine = make_engine()

    assert engine.summary() == {
        "headwords": 0,
        "lemmas": 0,
        "contexts": 0,
        "sources": 0,
    }


# =========================================================
# String Representation
# =========================================================


def test_string_representation_contains_engine_name():
    engine = make_engine()

    text = str(engine)

    assert "LexicalLookupEngine" in text


def test_string_representation_mentions_index_domains():
    engine = make_engine()

    text = str(engine)

    assert "Headword" in text
    assert "Lemma" in text
    assert "Context" in text
    assert "Source" in text
    

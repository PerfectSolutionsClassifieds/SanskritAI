
from types import SimpleNamespace

from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)
from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)
from SanskritAI.acquisition.knowledge.indexes.knowledge_index import (
    KnowledgeIndex,
)
from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)
from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
)


def make_knowledge_index():
    return KnowledgeIndex(
        headword_index=HeadwordIndex(),
        lemma_index=LemmaIndex(),
        context_index=ContextIndex(),
        source_index=SourceIndex(),
        lookup_engine=SimpleNamespace(),
    )


def make_entry(headword: str):
    return SimpleNamespace(headword=headword)


def make_lemma(
    lemma_id: str,
    text: str,
):
    return SimpleNamespace(
        lemma_id=lemma_id,
        text=text,
    )


def make_context(identifier: str):
    return SimpleNamespace(identifier=identifier)


def make_source(source_id: str):
    return SimpleNamespace(source_id=source_id)


def make_sense(name: str):
    return SimpleNamespace(name=name)


def test_knowledge_index_contains_all_component_indexes():
    index = make_knowledge_index()

    assert isinstance(index.headword_index, HeadwordIndex)
    assert isinstance(index.lemma_index, LemmaIndex)
    assert isinstance(index.context_index, ContextIndex)
    assert isinstance(index.source_index, SourceIndex)
    assert index.lookup_engine is not None


def test_summary_reports_all_index_counts():
    index = make_knowledge_index()

    index.headword_index.add(
        make_entry("राम")
    )

    index.lemma_index.add(
        make_lemma("L1", "राम")
    )

    index.context_index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )

    index.source_index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )

    assert index.summary() == {
        "headwords": 1,
        "lemmas": 1,
        "contexts": 1,
        "sources": 1,
    }


def test_summary_reports_zero_for_empty_indexes():
    index = make_knowledge_index()

    assert index.summary() == {
        "headwords": 0,
        "lemmas": 0,
        "contexts": 0,
        "sources": 0,
    }


def test_clear_propagates_to_all_indexes():
    index = make_knowledge_index()

    index.headword_index.add(
        make_entry("राम")
    )

    index.lemma_index.add(
        make_lemma("L1", "राम")
    )

    index.context_index.add(
        make_context("chapter-1"),
        make_sense("sense-1"),
    )

    index.source_index.add(
        make_source("MW"),
        make_sense("sense-1"),
    )

    index.clear()

    assert len(index.headword_index) == 0
    assert len(index.lemma_index) == 0
    assert len(index.context_index) == 0
    assert len(index.source_index) == 0

    assert index.summary() == {
        "headwords": 0,
        "lemmas": 0,
        "contexts": 0,
        "sources": 0,
    }


def test_clear_does_not_replace_component_indexes():
    index = make_knowledge_index()

    headword_index = index.headword_index
    lemma_index = index.lemma_index
    context_index = index.context_index
    source_index = index.source_index

    index.clear()

    assert index.headword_index is headword_index
    assert index.lemma_index is lemma_index
    assert index.context_index is context_index
    assert index.source_index is source_index


def test_string_representation_contains_summary():
    index = make_knowledge_index()

    assert str(index) == (
        "KnowledgeIndex("
        "{'headwords': 0, "
        "'lemmas': 0, "
        "'contexts': 0, "
        "'sources': 0}"
        ")"
    )


def test_indexes_can_be_populated_independently():
    index = make_knowledge_index()

    entry = make_entry("राम")
    lemma = make_lemma("L1", "राम")
    context = make_context("chapter-1")
    source = make_source("MW")
    sense = make_sense("sense-1")

    index.headword_index.add(entry)
    index.lemma_index.add(lemma)
    index.context_index.add(context, sense)
    index.source_index.add(source, sense)

    assert index.headword_index.lookup("राम") is entry
    assert index.lemma_index.lookup("L1") is lemma
    assert index.context_index.lookup("chapter-1") == (sense,)
    assert index.source_index.lookup("MW") == (sense,)


def test_knowledge_index_is_slot_based():
    index = make_knowledge_index()

    assert not hasattr(index, "__dict__")


def test_component_indexes_are_independent():
    first = make_knowledge_index()
    second = make_knowledge_index()

    first.headword_index.add(
        make_entry("राम")
    )

    assert len(first.headword_index) == 1
    assert len(second.headword_index) == 0

    


from __future__ import annotations

from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)
from SanskritAI.acquisition.knowledge.builders.canonical_knowledge_repository_builder import (
    CanonicalKnowledgeRepositoryBuilder,
)
from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)
from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)
from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)
from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)


# ============================================================
# Test Data
# ============================================================

def make_record(
    headword: str,
    record_id: str,
) -> CanonicalLexicalRecord:
    return CanonicalLexicalRecord(
        headword=headword,
        definition=f"Definition of {headword}",
        language="Sanskrit",
        script="Devanagari",
        entry_type="lexical",
        source_name="Test Source",
        source_version="1.0",
        source_record_id=record_id,
    )


def make_lexicon(
    identifier: str = "test-lexicon",
    name: str = "Test Lexicon",
    version: str = "1.0",
) -> CanonicalLexicon:
    source = CanonicalSource(
        source_id="test-source",
        name="Test Source",
        short_name="TEST",
    )

    lemma_ram = CanonicalLemma(
        lemma="राम",
        transliteration="rāma",
    )

    lemma_hari = CanonicalLemma(
        lemma="हरि",
        transliteration="hari",
    )

    context_ram = CanonicalContext(
        corpus="Purāṇa",
        work="Rāmāyaṇa",
        chapter="1",
        verse="1",
    )

    context_hari = CanonicalContext(
        corpus="Purāṇa",
        work="Rāmāyaṇa",
        chapter="1",
        verse="2",
    )

    sense_ram = CanonicalDictionarySense(
        sense_id="ram-1",
        entry_headword="राम",
        definition="Rāma",
        context=context_ram,
        source=source,
    )

    sense_hari = CanonicalDictionarySense(
        sense_id="hari-1",
        entry_headword="हरि",
        definition="Hari",
        context=context_hari,
        source=source,
    )

    entry_ram = CanonicalDictionaryEntry(
        headword="राम",
        transliteration="rāma",
        lemma=lemma_ram,
        senses=(sense_ram,),
        source_name="Test Source",
        source_version="1.0",
        source_record_id="ram-1",
    )

    entry_hari = CanonicalDictionaryEntry(
        headword="हरि",
        transliteration="hari",
        lemma=lemma_hari,
        senses=(sense_hari,),
        source_name="Test Source",
        source_version="1.0",
        source_record_id="hari-1",
    )

    return CanonicalLexicon(
        identifier=identifier,
        name=name,
        version=version,
        language="Sanskrit",
        entries={
            "राम": entry_ram,
            "हरि": entry_hari,
        },
    )


def make_index_builder() -> CanonicalIndexBuilder:
    return CanonicalIndexBuilder()


# ============================================================
# Canonical Record → Lexicon
# ============================================================

def test_canonical_records_can_be_represented_as_lexicon():
    records = (
        make_record("राम", "ram-1"),
        make_record("हरि", "hari-1"),
        make_record("शिव", "shiva-1"),
    )

    assert len(records) == 3

    lexicon = make_lexicon()

    assert isinstance(lexicon, CanonicalLexicon)
    assert lexicon.identifier == "test-lexicon"
    assert lexicon.name == "Test Lexicon"
    assert lexicon.version == "1.0"


# ============================================================
# Canonical Object Graph
# ============================================================

def test_canonical_lexicon_contains_entries():
    lexicon = make_lexicon()

    entries = lexicon.all_entries()

    assert len(entries) == 2
    assert lexicon.contains("राम")
    assert lexicon.contains("हरि")

    assert lexicon.get("राम") is not None
    assert lexicon.get("हरि") is not None


def test_canonical_entries_contain_contexts_and_sources():
    lexicon = make_lexicon()

    contexts = lexicon.all_contexts()
    sources = lexicon.all_sources()

    assert len(contexts) == 2
    assert len(sources) == 1

    assert all(
        isinstance(context, CanonicalContext)
        for context in contexts
    )

    assert all(
        isinstance(source, CanonicalSource)
        for source in sources
    )


# ============================================================
# Repository Builder Integration
# ============================================================

def test_repository_builder_populates_repository_and_indexes():
    repository = CanonicalKnowledgeRepository()
    index_builder = make_index_builder()

    builder = CanonicalKnowledgeRepositoryBuilder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    result = builder.build((lexicon,))

    assert result is repository

    lexical_repository = repository.lexical_repository

    assert lexical_repository is not None

    registered = lexical_repository.all()

    assert len(registered) == 1
    assert registered[0] is lexicon

    assert repository.lexical_repository.get_entry("राम") is not None
    assert repository.lexical_repository.get_entry("हरि") is not None


# ============================================================
# Knowledge Index Integration
# ============================================================

def test_repository_builder_populates_lookup_indexes():
    repository = CanonicalKnowledgeRepository()
    index_builder = make_index_builder()

    builder = CanonicalKnowledgeRepositoryBuilder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.build((lexicon,))

    assert index_builder.headword_index.lookup("राम")
    assert index_builder.headword_index.lookup("हरि")

    assert index_builder.lemma_index.lookup("राम")
    assert index_builder.lemma_index.lookup("हरि")

    assert index_builder.context_index.lookup(
        lexicon.get("राम").senses[0].context
    )

    assert index_builder.source_index.lookup(
        lexicon.get("राम").senses[0].source
    )


# ============================================================
# Rebuild / Replacement Semantics
# ============================================================

def test_repository_builder_rebuild_replaces_previous_state():
    repository = CanonicalKnowledgeRepository()
    index_builder = make_index_builder()

    builder = CanonicalKnowledgeRepositoryBuilder(
        repository=repository,
        index_builder=index_builder,
    )

    first = make_lexicon(
        identifier="lexicon-1",
        name="First Lexicon",
    )

    second = make_lexicon(
        identifier="lexicon-2",
        name="Second Lexicon",
    )

    builder.build((first,))

    registered = repository.lexical_repository.all()

    assert len(registered) == 1
    assert registered[0] is first

    builder.build((second,))

    registered = repository.lexical_repository.all()

    assert len(registered) == 1
    assert registered[0] is second
    assert first not in registered


# ============================================================
# Multiple Lexicons
# ============================================================

def test_repository_builder_accepts_multiple_lexicons():
    repository = CanonicalKnowledgeRepository()
    index_builder = make_index_builder()

    builder = CanonicalKnowledgeRepositoryBuilder(
        repository=repository,
        index_builder=index_builder,
    )

    first = make_lexicon(
        identifier="lexicon-1",
        name="First Lexicon",
    )

    second = make_lexicon(
        identifier="lexicon-2",
        name="Second Lexicon",
    )

    builder.build(
        (
            first,
            second,
        )
    )

    registered = repository.lexical_repository.all()

    assert len(registered) == 2
    assert first in registered
    assert second in registered


# ============================================================
# Canonical Graph Traversal
# ============================================================

def test_repository_exposes_canonical_lexical_graph():
    repository = CanonicalKnowledgeRepository()
    index_builder = make_index_builder()

    builder = CanonicalKnowledgeRepositoryBuilder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.build((lexicon,))

    entry = repository.lexical_repository.get_entry("राम")

    assert entry is not None
    assert entry.headword == "राम"
    assert entry.lemma.lemma == "राम"

    sense = entry.senses[0]

    assert sense.entry_headword == "राम"
    assert sense.context is not None
    assert sense.source is not None


# ============================================================
# End-to-End Canonical Knowledge Construction
# ============================================================

def test_canonical_knowledge_build_is_end_to_end():
    repository = CanonicalKnowledgeRepository()
    index_builder = make_index_builder()

    builder = CanonicalKnowledgeRepositoryBuilder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    result = builder.build((lexicon,))

    assert result is repository

    entry = repository.lexical_repository.get_entry("राम")

    assert entry is not None
    assert entry.headword == "राम"

    sense = entry.senses[0]

    assert sense.context.corpus == "Purāṇa"
    assert sense.context.work == "Rāmāyaṇa"
    assert sense.context.chapter == "1"
    assert sense.context.verse == "1"

    assert sense.source.name == "Test Source"
    assert sense.source.short_name == "TEST"

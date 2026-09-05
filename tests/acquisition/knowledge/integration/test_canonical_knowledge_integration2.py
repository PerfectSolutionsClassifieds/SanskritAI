
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
from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)
from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)
from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)
from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
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
from SanskritAI.acquisition.knowledge.registries.lemma_registry import (
    LemmaRegistry,
)
from SanskritAI.acquisition.knowledge.registries.lexical_registry import (
    LexicalRegistry,
)
from SanskritAI.acquisition.knowledge.registries.source_registry import (
    SourceRegistry,
)


def make_records() -> tuple[CanonicalLexicalRecord, ...]:
    return (
        CanonicalLexicalRecord(
            headword="राम",
            transliteration="rāma",
            definition="राम proper name Rama",
            entry_type="noun",
            source_name="Monier-Williams",
            source_version="test-1.0",
            source_record_id="MW-राम",
        ),
        CanonicalLexicalRecord(
            headword="हरि",
            transliteration="hari",
            definition="हरि Vishnu Hari",
            entry_type="noun",
            source_name="Monier-Williams",
            source_version="test-1.0",
            source_record_id="MW-हरि",
        ),
        CanonicalLexicalRecord(
            headword="शिव",
            transliteration="śiva",
            definition="शिव auspicious Shiva",
            entry_type="adjective",
            source_name="Monier-Williams",
            source_version="test-1.0",
            source_record_id="MW-शिव",
        ),
    )


def make_lexicon() -> CanonicalLexicon:
    records = make_records()

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams Sanskrit-English Dictionary",
        short_name="MW",
        source_type="lexicon",
        author="Monier-Williams",
        publication_year=1899,
        version="test-1.0",
    )

    entries = {}

    for record in records:
        lemma = CanonicalLemma(
            lemma=record.headword,
            transliteration=record.transliteration,
            part_of_speech=record.entry_type,
        )

        context = CanonicalContext(
            corpus="Integration",
            work="Test Lexicon",
            chapter="1",
            verse=record.source_record_id,
        )

        sense = CanonicalDictionarySense(
            sense_id=f"{record.source_name}:{record.source_record_id}",
            entry_headword=record.headword,
            definition=record.definition,
            context=context,
            source=source,
            part_of_speech=record.entry_type,
        )

        entry = CanonicalDictionaryEntry(
            headword=record.headword,
            transliteration=record.transliteration,
            lemma=lemma,
            entry_type=record.entry_type,
            senses=(sense,),
            source_name=record.source_name,
            source_version=record.source_version,
            source_record_id=record.source_record_id,
        )

        entries[record.headword] = entry

    return CanonicalLexicon(
        identifier="mw.integration",
        name="Monier-Williams Integration Lexicon",
        version="test-1.0",
        language="sa",
        source="Monier-Williams",
        entries=entries,
    )


def make_index_builder() -> CanonicalIndexBuilder:
    return CanonicalIndexBuilder(
        headword_index=HeadwordIndex(),
        lemma_index=LemmaIndex(),
        context_index=ContextIndex(),
        source_index=SourceIndex(),
    )


def test_canonical_lexical_records_become_canonical_lexicon():
    lexicon = make_lexicon()

    assert isinstance(lexicon, CanonicalLexicon)
    assert lexicon.identifier == "mw.integration"
    assert lexicon.entry_count == 3
    assert lexicon.sense_count == 3

    assert lexicon.contains("राम")
    assert lexicon.contains("हरि")
    assert lexicon.contains("शिव")

    rama = lexicon.get("राम")

    assert rama is not None
    assert rama.lemma_text == "राम"
    assert rama.sense_count == 1
    assert rama.primary_sense() is not None


def test_canonical_lexicon_graph_contains_contexts_and_sources():
    lexicon = make_lexicon()

    contexts = tuple(lexicon.all_contexts())
    sources = tuple(lexicon.all_sources())

    assert len(contexts) == 3
    assert len(sources) == 1

    assert contexts[0].corpus == "Integration"
    assert sources[0].source_id == "mw"
    assert sources[0].is_lexicon is True


# def test_repository_builder_populates_repository_and_indexes():
#     repository = CanonicalKnowledgeRepository()
#     index_builder = make_index_builder()

#     builder = CanonicalKnowledgeRepositoryBuilder(
#         repository=repository,
#         index_builder=index_builder,
#     )

#     lexicon = make_lexicon()

#     result = builder.build((lexicon,))

#     assert result is repository

#     registered = repository.lexical_repository.all()

#     assert len(registered) == 1
#     assert registered[0] is lexicon

#     assert index_builder.headword_index.lookup("राम") is lexicon.get("राम")
#     assert index_builder.headword_index.lookup("हरि") is lexicon.get("हरि")
#     assert index_builder.headword_index.lookup("शिव") is lexicon.get("शिव")

#     assert index_builder.lemma_index.lookup("राम") is not None
#     assert index_builder.lemma_index.lookup("हरि") is not None
#     assert index_builder.lemma_index.lookup("शिव") is not None

#     assert len(index_builder.context_index) == 3
#     assert len(index_builder.source_index) == 1

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

    registered = repository.lexical_registry.all()

    assert len(registered) == 1
    assert registered[0] is lexicon

    assert repository.knowledge_index.headword.lookup("राम") is not None
    assert repository.knowledge_index.lemma.lookup("राम") is not None

def test_canonical_registries_register_object_graph_components():
    lexicon = make_lexicon()

    lexical_registry = LexicalRegistry()
    lemma_registry = LemmaRegistry()
    source_registry = SourceRegistry()

    lexical_registry.register(lexicon)

    for entry in lexicon.all_entries():
        if entry.lemma is not None:
            lemma_registry.register(entry.lemma)

        for sense in entry:
            if sense.source is not None:
                source_registry.register(sense.source)

    assert lexical_registry.lookup("mw.integration") is lexicon

    assert lemma_registry.lookup("राम") is not None
    assert lemma_registry.lookup("हरि") is not None
    assert lemma_registry.lookup("शिव") is not None

    assert source_registry.lookup("mw") is not None
    assert source_registry.lookup_by_short_name("MW") is not None


def test_index_rebuild_replaces_previous_canonical_state():
    builder = make_index_builder()

    first = make_lexicon()

    builder.build((first,))

    assert builder.headword_index.lookup("राम") is not None

    second = CanonicalLexicon(
        identifier="second.lexicon",
        name="Second Lexicon",
        version="1.0",
        entries={
            "गम्": CanonicalDictionaryEntry(
                headword="गम्",
                lemma=CanonicalLemma(
                    lemma="गम्",
                ),
                senses=(
                    CanonicalDictionarySense(
                        sense_id="second:gām",
                        entry_headword="गम्",
                        definition="to go",
                    ),
                ),
            ),
        },
    )

    builder.build((second,))

    assert builder.headword_index.lookup("राम") is None
    assert builder.headword_index.lookup("गम्") is not None
    assert builder.lemma_index.lookup("गम्") is not None


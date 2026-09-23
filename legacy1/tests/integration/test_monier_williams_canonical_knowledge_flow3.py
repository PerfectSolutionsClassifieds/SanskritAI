
from __future__ import annotations

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)

from SanskritAI.domain.lexical.adapters.in_memory_monier_williams_adapter import (
    InMemoryMonierWilliamsAdapter,
)

from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.domain.lexical.default_lexical_repository import (
    DefaultLexicalRepository,
)

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


def make_source_record() -> MonierWilliamsSourceRecord:
    """Create a deterministic MW acquisition-stage source record."""

    return MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="हरि । विष्णु; monkey; lion",
        fields={
            "headword": "हरि",
            "transliteration": "hari",
            "definition": "Vishnu; monkey; lion",
            "grammatical_label": "m.",
            "grammatical_category": "noun",
            "source": "monier-williams",
            "source_id": "MW-हरि-001",
            "source_reference": "MW s.v. हरि",
            "homonym": "1",
        },
    )


def make_canonical_lexicon(
    entry: CanonicalDictionaryEntry,
) -> CanonicalLexicon:
    """Create a canonical lexicon containing one MW entry."""

    return CanonicalLexicon(
        identifier="monier-williams.integration",
        name="Monier-Williams Integration Test",
        version="test-1.0",
        language="sa",
        description="Deterministic MW canonical integration fixture.",
        source="Monier-Williams",
        entries={
            entry.headword: entry,
        },
    )


def test_source_record_to_adapter_record_boundary():
    """
    Acquisition SourceRecord
        ->
    InMemoryMonierWilliamsAdapter
        ->
    MonierWilliamsRecord
    """

    source_record = make_source_record()

    adapter = InMemoryMonierWilliamsAdapter.from_source_records(
        (source_record,),
    )

    records = adapter.all_records()

    assert len(records) == 1

    record = records[0]

    assert record.headword == "हरि"
    assert record.transliteration == "hari"
    assert record.definition == "Vishnu; monkey; lion"
    assert record.grammatical_label == "m."
    assert record.grammatical_category == "noun"
    assert record.source == "monier-williams"
    assert record.source_id == "MW-हरि-001"
    assert record.source_reference == "MW s.v. हरि"

    assert not isinstance(
        record,
        CanonicalDictionaryEntry,
    )

    assert not isinstance(
        record,
        CanonicalDictionarySense,
    )


def test_adapter_record_to_canonical_entry_and_sense():
    """
    MonierWilliamsRecord
        ->
    MonierWilliamsMapper
        ->
    CanonicalDictionaryEntry
    CanonicalDictionarySense
    CanonicalSource
    """

    source_record = make_source_record()

    adapter = InMemoryMonierWilliamsAdapter.from_source_records(
        (source_record,),
    )

    record = adapter.all_records()[0]

    entry, sense = MonierWilliamsMapper.to_entry_and_sense(
        record,
    )

    assert isinstance(
        entry,
        CanonicalDictionaryEntry,
    )

    assert isinstance(
        sense,
        CanonicalDictionarySense,
    )

    assert isinstance(
        sense.source,
        CanonicalSource,
    )

    assert entry.headword == "हरि"
    assert entry.transliteration == "hari"
    assert entry.lemma == "हरि"
    assert entry.language == "sa"
    assert entry.script == "Devanagari"

    assert entry.source_name == "monier-williams"
    assert entry.source_version == "unknown"
    assert entry.source_record_id == "MW-हरि-001"

    assert entry.sense_count == 1
    assert entry.senses[0] is sense

    assert sense.entry_headword == "हरि"
    assert sense.definition == "Vishnu; monkey; lion"
    assert sense.part_of_speech == "m."

    assert sense.identifier == "MW-हरि-001:1"

    assert sense.source is not None
    assert sense.source.source_id == "monier-williams"
    assert sense.source.name == "Monier-Williams"
    assert sense.source.short_name == "MW"
    assert sense.source.source_type == "lexicon"
    assert sense.source.language == "sa"


def test_canonical_lexicon_to_knowledge_repository_to_domain_repository():
    """
    CanonicalDictionaryEntry
        ->
    CanonicalLexicon
        ->
    CanonicalKnowledgeRepository
        ->
    DefaultLexicalRepository
    """

    source_record = make_source_record()

    adapter = InMemoryMonierWilliamsAdapter.from_source_records(
        (source_record,),
    )

    record = adapter.all_records()[0]

    entry, sense = MonierWilliamsMapper.to_entry_and_sense(
        record,
    )

    lexicon = make_canonical_lexicon(
        entry,
    )

    repository = CanonicalKnowledgeRepository()

    repository.add_lexicon(
        lexicon,
    )

    assert repository.lexical_entry_count == 1

    canonical_entry = repository.get_entry(
        "हरि",
    )

    assert canonical_entry is entry
    assert canonical_entry.headword == "हरि"
    assert canonical_entry.sense_count == 1

    canonical_senses = repository.find_senses(
        "हरि",
    )

    assert len(canonical_senses) == 1
    assert canonical_senses[0] is sense

    domain_repository = DefaultLexicalRepository(
        repository=repository,
    )

    assert domain_repository.get_entry(
        "हरि",
    ) is entry

    assert domain_repository.find_entries_by_word_form(
        "हरि",
    ) == (entry,)

    assert domain_repository.find_entries_by_lemma(
        "हरि",
    ) == (entry,)

    assert domain_repository.find_senses(
        "हरि",
    ) == (sense,)


def test_complete_monier_williams_canonical_knowledge_flow():
    """
    Complete integration contract:

    Acquisition SourceRecord
        ->
    MW Adapter
        ->
    MW normalized Record
        ->
    MW Mapper
        ->
    Canonical Entry / Sense / Source
        ->
    Canonical Lexicon
        ->
    Canonical Knowledge Repository
        ->
    Default Lexical Repository
        ->
    Domain Lexical Lookup Engine
        ->
    Lexical Resolution Result
    """

    # ---------------------------------------------------------
    # 1. Acquisition boundary
    # ---------------------------------------------------------

    source_record = make_source_record()

    # ---------------------------------------------------------
    # 2. Acquisition -> normalized lexical representation
    # ---------------------------------------------------------

    adapter = InMemoryMonierWilliamsAdapter.from_source_records(
        (source_record,),
    )

    normalized_records = adapter.all_records()

    assert len(normalized_records) == 1

    record = normalized_records[0]

    assert record.headword == "हरि"

    # ---------------------------------------------------------
    # 3. Normalized representation -> canonical representation
    # ---------------------------------------------------------

    entry, sense = MonierWilliamsMapper.to_entry_and_sense(
        record,
    )

    assert isinstance(
        entry,
        CanonicalDictionaryEntry,
    )

    assert isinstance(
        sense,
        CanonicalDictionarySense,
    )

    assert entry.headword == "हरि"
    assert entry.senses[0] is sense

    # ---------------------------------------------------------
    # 4. Canonical lexical state
    # ---------------------------------------------------------

    lexicon = make_canonical_lexicon(
        entry,
    )

    canonical_repository = CanonicalKnowledgeRepository()

    canonical_repository.add_lexicon(
        lexicon,
    )

    assert canonical_repository.lexical_entry_count == 1

    canonical_entry = canonical_repository.get_entry(
        "हरि",
    )

    assert canonical_entry is entry

    canonical_senses = canonical_repository.find_senses(
        "हरि",
    )

    assert len(canonical_senses) == 1
    assert canonical_senses[0] is sense

    # ---------------------------------------------------------
    # 5. Domain repository adapter
    # ---------------------------------------------------------

    lexical_repository = DefaultLexicalRepository(
        repository=canonical_repository,
    )

    assert lexical_repository.get_entry(
        "हरि",
    ) is entry

    domain_entries = lexical_repository.find_entries_by_word_form(
        "हरि",
    )

    assert domain_entries == (entry,)

    # ---------------------------------------------------------
    # 6. Domain lexical lookup
    # ---------------------------------------------------------

    lookup_engine = LexicalLookupEngine(
        repository=lexical_repository,
    )

    context = ResolutionContext(
        identifier="integration:mw:हरि",
        subject="हरि",
        source="monier-williams",
        language="sa",
        script="Devanagari",
    )

    result = lookup_engine.lookup(
        context,
    )

    # ---------------------------------------------------------
    # 7. Lookup contract
    #
    # IMPORTANT:
    #
    # The existing domain contract distinguishes between:
    #
    #   succeeded
    #       =
    #   lookup operation completed successfully
    #
    # and:
    #
    #   resolved
    #       =
    #   candidate satisfied the existing resolution policy
    #
    # This integration test owns the former boundary, not the
    # resolution-policy decision.
    # ---------------------------------------------------------

    assert result.succeeded

    assert result.has_candidates
    assert result.candidate_count == 1

    assert result.matched_word_form == "हरि"
    assert result.normalized_word_form == "हरि"

    # ---------------------------------------------------------
    # 8. Canonical object propagation
    #
    # The important architectural assertion is that the object
    # returned through the domain lookup originated from the
    # canonical knowledge repository.
    # ---------------------------------------------------------

    assert result.preferred_entry is entry
    assert result.preferred_sense is sense

    assert result.headword == "हरि"
    assert result.lemma == "हरि"
    assert result.definition == "Vishnu; monkey; lion"

    # ---------------------------------------------------------
    # 9. Canonical provenance propagation
    # ---------------------------------------------------------

    assert result.canonical_source is not None

    assert (
        result.canonical_source.source_id
        == "monier-williams"
    )

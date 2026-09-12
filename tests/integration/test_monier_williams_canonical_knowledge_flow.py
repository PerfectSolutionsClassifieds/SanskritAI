from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams -> Canonical Knowledge -> Domain Lexical
Integration Contract

Purpose
-------
Verify the complete Monier-Williams canonical knowledge flow:

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

This test intentionally verifies architectural propagation
without imposing a stronger resolution policy than the current
LexicalLookupEngine contract provides.
"""

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


# =============================================================
# Test Fixtures / Helpers
# =============================================================


# def make_source_record() -> MonierWilliamsSourceRecord:
#     """
#     Create a minimal Monier-Williams acquisition source record.
#     """

#     return MonierWilliamsSourceRecord(
#         entry_id="mw:hari",
#         headword="हरि",
#         transliteration="hari",
#         definition="Vishnu; monkey; lion",
#         raw_text="हरि",
#     )

def make_source_record() -> MonierWilliamsSourceRecord:
    """
    Create a minimal Monier-Williams acquisition source record.

    The acquisition record preserves raw source fields. The adapter
    is responsible for converting this into MonierWilliamsRecord.
    """
    return MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="हरि",
        fields={
            "headword": "हरि",
            "transliteration": "hari",
            "definition": "Vishnu; monkey; lion",
            "source_id": "mw:hari",
        },
        entry_id="mw:hari",
    )

def make_canonical_lexicon(
    entry: CanonicalDictionaryEntry,
) -> CanonicalLexicon:
    """
    Create a canonical lexicon containing the supplied entry.
    """

    return CanonicalLexicon(
        identifier="monier-williams",
        name="Monier-Williams Sanskrit-English Dictionary",
        version="1899",
        entries={
            entry.headword: entry,
        },
    )


# =============================================================
# 1. SourceRecord -> Adapter -> Normalized Record
# =============================================================


def test_source_record_to_normalized_record():
    """
    Verify the acquisition boundary.

    SourceRecord
        ->
    InMemoryMonierWilliamsAdapter
        ->
    MonierWilliamsRecord
    """

    source_record = make_source_record()

    adapter = InMemoryMonierWilliamsAdapter.from_source_records(
        (source_record,),
    )

    normalized_records = adapter.all_records()

    assert len(normalized_records) == 1

    record = normalized_records[0]

    assert record.headword == "हरि"


# =============================================================
# 2. Normalized Record -> Canonical Entry / Sense
# =============================================================


def test_normalized_record_to_canonical_entry_and_sense():
    """
    Verify the canonical mapping boundary.
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

    assert entry.headword == "हरि"

    assert entry.senses[0] is sense


# =============================================================
# 3. Canonical Entry / Sense -> Canonical Knowledge Repository
# =============================================================


def test_canonical_lexicon_to_canonical_knowledge_repository():
    """
    Verify canonical lexical state propagation.
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


# =============================================================
# 4. Complete Canonical Knowledge -> Domain Lookup Flow
# =============================================================


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

    domain_entries = (
        lexical_repository.find_entries_by_word_form(
            "हरि",
        )
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
    # This integration test verifies successful lookup and
    # canonical object propagation. It does not impose a
    # resolution-policy decision.
    # ---------------------------------------------------------

    assert result.succeeded

    assert result.has_candidates

    assert result.candidate_count == 1

    assert result.matched_word_form == "हरि"

    assert result.normalized_word_form == "हरि"

    # ---------------------------------------------------------
    # 8. Canonical entry propagation
    #
    # The lookup result must retain the canonical dictionary
    # entry originating from CanonicalKnowledgeRepository.
    #
    # The current LexicalLookupEngine attaches the entry to
    # LookupCandidate but does not attach a preferred sense.
    # Therefore sense-level properties are verified through
    # the canonical repository/sense assertions above.
    # ---------------------------------------------------------

    assert result.preferred_entry is entry

    assert result.headword == "हरि"

    assert result.lemma == "हरि"

    assert result.preferred_sense is None

    # ---------------------------------------------------------
    # 9. Canonical sense itself remains intact
    # ---------------------------------------------------------

    assert sense.definition == "Vishnu; monkey; lion"

    assert sense.source is not None

    assert sense.source.source_id == "monier-williams"

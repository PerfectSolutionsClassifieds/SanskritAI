
from __future__ import annotations

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)
from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


def make_record(
    headword: str = "राम",
    transliteration: str = "rāma",
    definition: str = "Rama",
    source_id: str = "MW-001",
) -> MonierWilliamsRecord:

    return MonierWilliamsRecord(
        headword=headword,
        transliteration=transliteration,
        definition=definition,
        grammatical_label="m.",
        grammatical_category="noun",
        source="Monier-Williams",
        source_id=source_id,
        source_reference="MW:001",
        raw_text="राम — Rama",
        homonym="1",
    )


# ============================================================
# Mapper → Sense
# ============================================================

def test_mapper_creates_canonical_sense():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(
        record
    )

    assert isinstance(
        sense,
        CanonicalDictionarySense,
    )

    assert sense.entry_headword == "राम"
    assert sense.definition == "Rama"
    assert sense.part_of_speech == "m."

    assert sense.identifier == "MW-001:1"

    assert sense.metadata["entry_id"] == "MW-001"
    assert sense.metadata["sense_number"] == 1


# ============================================================
# Mapper → Entry
# ============================================================

def test_mapper_creates_canonical_entry():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)

    assert isinstance(
        entry,
        CanonicalDictionaryEntry,
    )

    assert entry.headword == "राम"
    assert entry.transliteration == "rāma"
    assert entry.lemma == "राम"

    assert entry.source_name == "Monier-Williams"
    assert entry.source_record_id == "MW-001"

    assert entry.sense_count == 1
    assert entry.primary_sense() is not None


def test_mapper_entry_owns_canonical_sense():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)

    sense = entry.primary_sense()

    assert isinstance(
        sense,
        CanonicalDictionarySense,
    )

    assert sense.entry_headword == entry.headword
    assert sense.definition == "Rama"


# ============================================================
# Mapper → Lexicon
# ============================================================

def test_mapper_entries_can_construct_canonical_lexicon():
    records = (
        make_record(
            headword="राम",
            source_id="MW-001",
        ),
        make_record(
            headword="हरि",
            transliteration="hari",
            definition="Hari",
            source_id="MW-002",
        ),
    )

    entries = MonierWilliamsMapper.to_entries(
        records
    )

    lexicon = CanonicalLexicon(
        identifier="mw.test",
        name="Monier-Williams Test",
        version="1.0.0",
        language="sa",
        source="Monier-Williams",
        entries={
            entry.headword: entry
            for entry in entries
        },
    )

    assert lexicon.entry_count == 2
    assert lexicon.sense_count == 2

    assert lexicon.get("राम") is not None
    assert lexicon.get("हरि") is not None


# ============================================================
# Mapper → Metadata
# ============================================================

def test_mapper_preserves_source_metadata():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)

    sense = entry.primary_sense()

    assert entry.metadata["source_reference"] == (
        "MW:001"
    )

    assert entry.metadata["grammatical_category"] == (
        "noun"
    )

    assert entry.metadata["homonym"] == "1"

    assert sense is not None

    assert sense.metadata["source_id"] == (
        "MW-001"
    )

    assert sense.metadata["source_reference"] == (
        "MW:001"
    )

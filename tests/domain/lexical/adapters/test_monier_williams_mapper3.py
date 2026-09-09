
from __future__ import annotations

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)
from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)

from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)
from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


def make_record() -> MonierWilliamsRecord:
    return MonierWilliamsRecord(
        headword="hari",
        transliteration="hari",
        definition="yellow, tawny; a name of Viṣṇu",
        grammatical_label="m.",
        grammatical_category="noun",
        source="monier-williams",
        source_id="MW-hari",
        source_reference="MW-1234",
        raw_text="<L>hari ...",
        homonym="1",
    )


# ============================================================
# Source
# ============================================================

def test_to_source_returns_canonical_source():
    record = make_record()

    source = MonierWilliamsMapper.to_source(record)

    assert isinstance(source, CanonicalSource)
    assert source.source_id == "monier-williams"
    assert source.name == "Monier-Williams"
    assert source.short_name == "MW"


# ============================================================
# Entry
# ============================================================

def test_to_entry_returns_canonical_dictionary_entry():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)

    assert isinstance(entry, CanonicalDictionaryEntry)

    assert entry.identifier == "MW-hari"
    assert entry.headword == "hari"
    assert entry.transliteration == "hari"
    assert entry.lemma == "hari"

    assert entry.source_name == "monier-williams"
    assert entry.source_record_id == "MW-hari"

    assert entry.sense_count == 1


def test_to_entry_owns_canonical_sense():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)

    sense = entry.primary_sense()

    assert isinstance(sense, CanonicalDictionarySense)

    assert sense.entry_headword == entry.headword
    assert sense.definition == (
        "yellow, tawny; a name of Viṣṇu"
    )


# ============================================================
# Sense
# ============================================================

def test_to_sense_returns_canonical_dictionary_sense():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(
        record,
        entry_id="MW-hari",
    )

    assert isinstance(
        sense,
        CanonicalDictionarySense,
    )

    assert sense.identifier == "MW-hari:1"
    assert sense.entry_headword == "hari"

    assert sense.definition == (
        "yellow, tawny; a name of Viṣṇu"
    )

    assert sense.part_of_speech == "m."

    assert sense.citation == "MW-1234"


def test_to_sense_can_derive_entry_id():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(record)

    assert sense.identifier == "MW-hari:1"
    assert sense.metadata["entry_id"] == "MW-hari"


def test_to_sense_accepts_explicit_sense_number():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(
        record,
        entry_id="MW-hari",
        sense_number=3,
    )

    assert sense.identifier == "MW-hari:3"
    assert sense.metadata["sense_number"] == 3


def test_to_sense_accepts_explicit_sense_id():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(
        record,
        entry_id="MW-hari",
        sense_id="MW-hari:special",
    )

    assert sense.identifier == "MW-hari:special"


# ============================================================
# Entry + Sense
# ============================================================

def test_to_entry_and_sense_returns_matching_pair():
    record = make_record()

    entry, sense = (
        MonierWilliamsMapper.to_entry_and_sense(
            record
        )
    )

    assert isinstance(
        entry,
        CanonicalDictionaryEntry,
    )

    assert isinstance(
        sense,
        CanonicalDictionarySense,
    )

    assert entry.identifier == "MW-hari"
    assert sense.identifier == "MW-hari:1"

    assert entry.primary_sense() is sense


def test_to_entry_and_sense_preserves_sense_number():
    record = make_record()

    entry, sense = (
        MonierWilliamsMapper.to_entry_and_sense(
            record,
            sense_number=4,
        )
    )

    assert entry.identifier == "MW-hari"
    assert sense.identifier == "MW-hari:4"
    assert sense.metadata["sense_number"] == 4


# ============================================================
# Batch
# ============================================================

def test_to_entries_returns_canonical_entries():
    records = (
        make_record(),
        MonierWilliamsRecord(
            headword="agni",
            transliteration="agni",
            definition="fire",
            grammatical_label="m.",
            grammatical_category="noun",
            source="monier-williams",
            source_id="MW-agni",
            source_reference="MW-5678",
            raw_text="<L>agni ...",
            homonym="1",
        ),
    )

    entries = MonierWilliamsMapper.to_entries(
        records
    )

    assert isinstance(entries, tuple)
    assert len(entries) == 2

    assert all(
        isinstance(
            entry,
            CanonicalDictionaryEntry,
        )
        for entry in entries
    )

    assert entries[0].identifier == "MW-hari"
    assert entries[1].identifier == "MW-agni"


# ============================================================
# Metadata Preservation
# ============================================================

def test_mapper_preserves_source_metadata():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)
    sense = entry.primary_sense()

    assert entry.metadata["source_reference"] == (
        "MW-1234"
    )

    assert entry.metadata["grammatical_category"] == (
        "noun"
    )

    assert entry.metadata["homonym"] == "1"

    assert sense is not None

    assert sense.metadata["source_id"] == (
        "MW-hari"
    )

    assert sense.metadata["source_reference"] == (
        "MW-1234"
    )


# ============================================================
# Validation
# ============================================================

def test_mapper_rejects_invalid_record():
    try:
        MonierWilliamsMapper.to_entry("invalid")
    except TypeError as exc:
        assert "MonierWilliamsRecord" in str(exc)
    else:
        raise AssertionError(
            "Expected TypeError"
        )


def test_mapper_rejects_empty_entry_id():
    record = make_record()

    try:
        MonierWilliamsMapper.to_sense(
            record,
            entry_id="",
        )
    except ValueError as exc:
        assert "entry_id" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError"
        )


def test_mapper_rejects_invalid_sense_number():
    record = make_record()

    try:
        MonierWilliamsMapper.to_sense(
            record,
            sense_number=0,
        )
    except ValueError as exc:
        assert "sense_number" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError"
        )

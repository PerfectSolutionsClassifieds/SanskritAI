
from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)
from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)
from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
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


def test_to_source_returns_canonical_lexical_source():
    record = make_record()

    source = MonierWilliamsMapper.to_source(record)

    assert isinstance(source, LexicalSource)
    assert source.identifier == "monier-williams"
    assert source.name == "Monier-Williams"


def test_to_entry_returns_canonical_dictionary_entry():
    record = make_record()

    entry = MonierWilliamsMapper.to_entry(record)

    assert isinstance(entry, DictionaryEntry)
    assert entry.identifier == "MW-hari"

    assert entry.dictionary_name == "Monier-Williams"
    assert entry.entry_identifier == "MW-hari"
    assert entry.headword == "hari"
    assert entry.transliteration == "hari"
    assert entry.metadata.language == "sa"


def test_to_sense_returns_canonical_dictionary_sense():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(
        record,
        entry_id="MW-hari",
    )

    assert isinstance(sense, DictionarySense)

    assert sense.identifier == "MW-hari:1"
    assert sense.sense_number == 1

    assert sense.definition == (
        "yellow, tawny; a name of Viṣṇu"
    )

    assert sense.usage_label == "m."
    assert sense.grammatical_note == "m.; noun"

    assert sense.citations == [
        "MW-1234"
    ]

    assert sense.metadata.language == "en"


def test_to_sense_accepts_explicit_sense_number():
    record = make_record()

    sense = MonierWilliamsMapper.to_sense(
        record,
        entry_id="MW-hari",
        sense_number=3,
    )

    assert sense.identifier == "MW-hari:3"
    assert sense.sense_number == 3


def test_to_entry_and_sense_returns_matching_pair():
    record = make_record()

    entry, sense = (
        MonierWilliamsMapper.to_entry_and_sense(
            record
        )
    )

    assert isinstance(entry, DictionaryEntry)
    assert isinstance(sense, DictionarySense)

    assert entry.identifier == "MW-hari"
    assert sense.identifier == "MW-hari:1"


def test_mapper_rejects_invalid_record():
    try:
        MonierWilliamsMapper.to_entry("invalid")
    except TypeError as exc:
        assert "MonierWilliamsRecord" in str(exc)
    else:
        raise AssertionError(
            "Expected TypeError"
        )

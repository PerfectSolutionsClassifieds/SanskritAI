
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)
from SanskritAI.domain.lexical.adapters import (
    MonierWilliamsAdapter,
    MonierWilliamsRecord,
)


def test_source_record_converts_to_monier_williams_record():
    source_record = MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="राम<TAB>rāma<TAB>Rama",
        fields={
            "k1": "  राम  ",
            "e": "  Rama  ",
            "transliteration": " rāma ",
            "h": "m.",
            "L": "1",
        },
    )

    record = MonierWilliamsAdapter.from_source_record(
        source_record
    )

    assert isinstance(
        record,
        MonierWilliamsRecord,
    )

    assert record.headword == "राम"
    assert record.definition == "Rama"
    assert record.transliteration == "rāma"
    assert record.grammatical_label == "m."
    assert record.homonym == "1"


def test_source_record_requires_headword():
    source_record = MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="invalid",
        fields={
            "e": "meaning",
        },
    )

    try:
        MonierWilliamsAdapter.from_source_record(
            source_record
        )
    except ValueError as exc:
        assert "headword" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for missing headword"
        )


def test_source_record_requires_definition():
    source_record = MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="invalid",
        fields={
            "k1": "राम",
        },
    )

    try:
        MonierWilliamsAdapter.from_source_record(
            source_record
        )
    except ValueError as exc:
        assert "definition" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for missing definition"
        )

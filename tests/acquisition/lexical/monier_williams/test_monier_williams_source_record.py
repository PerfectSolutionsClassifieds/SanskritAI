
import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsSourceRecord,
)


def test_source_record_exposes_fields():
    record = MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="<L>1\n<k1>rAma\n<LEND>",
        fields={
            "L": "1",
            "k1": "rAma",
            "e": "pleasing",
        },
    )

    assert record.sequence == 1
    assert record.headword == "rAma"
    assert record.get("e") == "pleasing"


def test_source_record_unknown_field_is_preserved():
    record = MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="<L>1\n<x>abc\n<LEND>",
        fields={"x": "abc"},
    )

    assert record.get("x") == "abc"


def test_source_record_requires_positive_sequence():
    with pytest.raises(ValueError):
        MonierWilliamsSourceRecord(
            sequence=0,
            raw_text="<L>1<LEND>",
            fields={},
        )


def test_source_record_requires_raw_text():
    with pytest.raises(ValueError):
        MonierWilliamsSourceRecord(
            sequence=1,
            raw_text=" ",
            fields={},
        )

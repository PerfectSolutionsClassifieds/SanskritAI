
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_parser import (
    MonierWilliamsSourceParser,
)

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)

from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


MW_SAMPLE = """\
<L>1
<k1>rAma
<k2>1
<h>m.
<e>pleasing, beautiful
<LEND>
"""


def test_source_record_is_explicitly_normalized_to_adapter_record():

    parser = MonierWilliamsSourceParser()

    records = parser.parse(MW_SAMPLE)

    assert len(records) == 1

    source_record = records[0]

    assert isinstance(
        source_record,
        MonierWilliamsSourceRecord,
    )

    normalized = (
        MonierWilliamsMapper.from_source_record(
            source_record
        )
    )

    assert isinstance(
        normalized,
        MonierWilliamsRecord,
    )

    assert normalized.headword == "rAma"
    assert normalized.definition == (
        "pleasing, beautiful"
    )

    assert normalized.grammatical_label == "m."

    assert normalized.source == (
        "monier-williams"
    )

    assert normalized.homonym == "1"

    assert normalized.raw_text.startswith(
        "<L>1"
    )


def test_source_record_preserves_source_id_when_present():

    source_record = MonierWilliamsSourceRecord(
        sequence=1,
        raw_text="raw",
        fields={
            "headword": "देव",
            "definition": "god",
            "source_id": "mw-001",
            "h": "m.",
        },
    )

    normalized = (
        MonierWilliamsMapper.from_source_record(
            source_record
        )
    )

    assert normalized.headword == "देव"
    assert normalized.definition == "god"
    assert normalized.source_id == "mw-001"
    assert normalized.grammatical_label == "m."


def test_source_record_rejects_invalid_boundary_input():

    try:
        MonierWilliamsMapper.from_source_record(
            object()
        )
    except TypeError as exc:
        assert (
            "MonierWilliamsSourceRecord"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected TypeError"
        )

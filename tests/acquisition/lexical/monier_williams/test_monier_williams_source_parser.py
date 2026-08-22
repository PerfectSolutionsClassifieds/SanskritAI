
import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsSourceParser,
)


MW_SAMPLE = """\
<L>1
<k1>rAma
<k2>1
<h>m.
<e>pleasing, beautiful
<LEND>
<L>2
<k1>hari
<h>m.
<e>yellow, tawny
<LEND>
"""


def test_parser_reads_multiple_records():
    parser = MonierWilliamsSourceParser()

    records = parser.parse(MW_SAMPLE)

    assert len(records) == 2


def test_parser_reads_headword():
    parser = MonierWilliamsSourceParser()

    records = parser.parse(MW_SAMPLE)

    assert records[0].headword == "rAma"
    assert records[1].headword == "hari"


def test_parser_reads_homonym():
    parser = MonierWilliamsSourceParser()

    record = parser.parse(MW_SAMPLE)[0]

    assert record.homonym == "1"


def test_parser_preserves_grammatical_field():
    parser = MonierWilliamsSourceParser()

    record = parser.parse(MW_SAMPLE)[0]

    assert record.get("h") == "m."


def test_parser_preserves_definition_field():
    parser = MonierWilliamsSourceParser()

    record = parser.parse(MW_SAMPLE)[0]

    assert record.get("e") == "pleasing, beautiful"


def test_parser_preserves_raw_record():
    parser = MonierWilliamsSourceParser()

    record = parser.parse(MW_SAMPLE)[0]

    assert "<k1>rAma" in record.raw_text
    assert "<LEND>" in record.raw_text


def test_parser_rejects_empty_source():
    parser = MonierWilliamsSourceParser()

    with pytest.raises(ValueError):
        parser.parse("")


def test_parser_rejects_unterminated_record():
    parser = MonierWilliamsSourceParser()

    with pytest.raises(ValueError):
        parser.parse(
            "<L>1\n"
            "<k1>rAma\n"
            "<e>meaning\n"
        )


def test_parser_rejects_orphan_lend():
    parser = MonierWilliamsSourceParser()

    with pytest.raises(ValueError):
        parser.parse("<LEND>\n")


def test_parser_rejects_source_without_records():
    parser = MonierWilliamsSourceParser()

    with pytest.raises(ValueError):
        parser.parse(
            "ordinary text without MW tags\n"
        )


def test_parse_record_requires_one_record():
    parser = MonierWilliamsSourceParser()

    record = parser.parse_record(
        "<L>1\n"
        "<k1>rAma\n"
        "<LEND>\n"
    )

    assert record.sequence == 1
    assert record.headword == "rAma"


from SanskritAI.lexical.monier_williams.parser import (
    MonierWilliamsParser,
)


def test_parser_reads_single_record():

    source = [
        "<L>123<pc>1,1<k1>agni<k2>agni<h>1<e>1",
        "<body>fire",
        "<LEND>",
    ]

    records = list(
        MonierWilliamsParser().parse(source)
    )

    assert len(records) == 1

    record = records[0]

    assert record.line_id == "123"
    assert record.page == "1,1"
    assert record.key1 == "agni"
    assert record.key2 == "agni"
    assert record.homonym == "1"
    assert record.entry_number == "1"


def test_parser_preserves_raw_text():

    source = [
        "<L>1<pc>1,1<k1>agni",
        "fire",
        "<LEND>",
    ]

    record = next(
        MonierWilliamsParser().parse(source)
    )

    assert "agni" in record.raw_text
    assert "fire" in record.raw_text
    assert "<LEND>" in record.raw_text


def test_parser_handles_multiple_records():

    source = [
        "<L>1<k1>agni",
        "fire",
        "<LEND>",
        "<L>2<k1>indra",
        "Indra",
        "<LEND>",
    ]

    records = list(
        MonierWilliamsParser().parse(source)
    )

    assert len(records) == 2

    assert records[0].key1 == "agni"
    assert records[1].key1 == "indra"

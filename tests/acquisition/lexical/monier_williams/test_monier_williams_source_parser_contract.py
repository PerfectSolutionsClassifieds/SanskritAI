
import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsSourceParser,
    MonierWilliamsSourceRecord,
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


class ListReturningParser:
    """
    Compatibility parser deliberately returning a list.

    The public MonierWilliamsSourceParser contract must normalize
    the parser result to a tuple.
    """

    def parse(self, source_text):
        parser = MonierWilliamsSourceParser()

        return list(
            parser.parse(source_text)
        )


class InvalidReturningParser:

    def parse(self, source_text):
        return "not-records"


class WrongRecordParser:

    def parse(self, source_text):
        return [object()]


def test_source_parser_returns_tuple():

    parser = MonierWilliamsSourceParser()

    records = parser.parse(MW_SAMPLE)

    assert isinstance(records, tuple)

    assert all(
        isinstance(
            record,
            MonierWilliamsSourceRecord,
        )
        for record in records
    )


def test_source_parser_normalizes_list_return():

    parser = MonierWilliamsSourceParser(
        parser=ListReturningParser()
    )

    records = parser.parse(MW_SAMPLE)

    assert isinstance(records, tuple)
    assert len(records) == 2

    assert records[0].headword == "rAma"
    assert records[1].headword == "hari"


def test_source_parser_rejects_invalid_parser_result():

    parser = MonierWilliamsSourceParser(
        parser=InvalidReturningParser()
    )

    with pytest.raises(
        TypeError,
        match="tuple or list",
    ):
        parser.parse(MW_SAMPLE)


def test_source_parser_rejects_wrong_record_type():

    parser = MonierWilliamsSourceParser(
        parser=WrongRecordParser()
    )

    with pytest.raises(
        TypeError,
        match="unsupported record type",
    ):
        parser.parse(MW_SAMPLE)


def test_parse_record_returns_source_record():

    parser = MonierWilliamsSourceParser()

    record = parser.parse_record(
        "<L>1\n"
        "<k1>rAma\n"
        "<e>pleasing\n"
        "<LEND>\n"
    )

    assert isinstance(
        record,
        MonierWilliamsSourceRecord,
    )

    assert record.sequence == 1
    assert record.headword == "rAma"
    assert record.get("e") == "pleasing"

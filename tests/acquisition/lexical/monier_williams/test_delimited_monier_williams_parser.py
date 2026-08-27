
from __future__ import annotations

import pytest

from SanskritAI.acquisition.lexical.monier_williams.delimited_monier_williams_parser import (
    DelimitedMonierWilliamsParser,
)
from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


def test_parser_reads_basic_record():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "rāma\tpleasing; beautiful\n"
    )

    entries = parser.parse(text)

    assert len(entries) == 1

    entry = entries[0]

    assert entry.headword == "rāma"
    assert entry.definition == "pleasing; beautiful"
    assert entry.source == "monier-williams"


def test_parser_reads_optional_fields():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\tgrammatical_category\t"
        "transliteration\tsource_reference\n"
        "rāma\tpleasing\tnoun\trāma\tMW\n"
    )

    entries = parser.parse(text)

    entry = entries[0]

    assert entry.grammatical_category == "noun"
    assert entry.transliteration == "rāma"
    assert entry.source_reference == "MW"


def test_parser_rejects_invalid_header():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "invalid\tdefinition\n"
        "rāma\tpleasing\n"
    )

    with pytest.raises(ValueError):
        parser.parse(text)


def test_parser_empty_source_returns_empty_tuple():
    parser = DelimitedMonierWilliamsParser()

    assert parser.parse("") == ()


def test_parser_whitespace_only_source_returns_empty_tuple():
    parser = DelimitedMonierWilliamsParser()

    assert parser.parse("   \n\t  ") == ()


def test_parser_returns_monier_williams_records():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
    )

    entries = parser.parse(text)

    assert isinstance(entries[0], MonierWilliamsRecord)


def test_parser_sets_source_to_monier_williams():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
    )

    entry = parser.parse(text)[0]

    assert entry.source == "monier-williams"

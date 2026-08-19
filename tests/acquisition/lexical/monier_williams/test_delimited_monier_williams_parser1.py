from __future__ import annotations

import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    DelimitedMonierWilliamsParser,
)

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


def test_parser_reads_single_record():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\ttransliteration\tdefinition\t"
        "grammatical_label\tsource_id\traw_text\n"
        "देव\tdeva\tgod\tm.\tmw-001\tदेव — god\n"
    )

    records = parser.parse(text)

    assert len(records) == 1

    record = records[0]

    assert isinstance(
        record,
        MonierWilliamsRecord,
    )

    assert record.headword == "देव"
    assert record.transliteration == "deva"
    assert record.definition == "god"
    assert record.grammatical_label == "m."
    assert record.source == "monier-williams"
    assert record.source_id == "mw-001"
    assert record.raw_text == "देव — god"


def test_parser_reads_multiple_records():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "देव\tgod\n"
        "राम\tRama\n"
    )

    records = parser.parse(text)

    assert len(records) == 2
    assert records[0].headword == "देव"
    assert records[1].headword == "राम"


def test_parser_returns_empty_tuple_for_empty_source():
    parser = DelimitedMonierWilliamsParser()

    assert parser.parse("") == ()
    assert parser.parse("   ") == ()


def test_parser_rejects_non_string_source():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(TypeError):
        parser.parse(None)


def test_parser_requires_header():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse("")


def test_parser_requires_headword_column():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "definition\n"
        "god\n"
    )

    with pytest.raises(ValueError):
        parser.parse(text)


def test_parser_requires_definition_column():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\n"
        "देव\n"
    )

    with pytest.raises(ValueError):
        parser.parse(text)


def test_parser_rejects_missing_headword_value():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "\tgod\n"
    )

    with pytest.raises(ValueError):
        parser.parse(text)


def test_parser_rejects_missing_definition_value():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "देव\t\n"
    )

    with pytest.raises(ValueError):
        parser.parse(text)


def test_parser_supports_custom_delimiter():
    parser = DelimitedMonierWilliamsParser(
        delimiter=",",
    )

    text = (
        "headword,definition\n"
        "deva,god\n"
    )

    records = parser.parse(text)

    assert len(records) == 1
    assert records[0].headword == "deva"


def test_parser_strips_field_values():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "  देव  \t  god  \n"
    )

    records = parser.parse(text)

    assert records[0].headword == "देव"
    assert records[0].definition == "god"

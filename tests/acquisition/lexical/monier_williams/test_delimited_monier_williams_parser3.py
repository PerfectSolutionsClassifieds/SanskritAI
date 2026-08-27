
import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    DelimitedMonierWilliamsParser,
)


def test_parser_reads_basic_record():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "rāma\tpleasing; beautiful\n"
    )

    entries = parser.parse(text)

    assert len(entries) == 1
    assert entries[0].headword == "rāma"
    assert entries[0].definition == "pleasing; beautiful"


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


def test_parser_requires_header():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse(
            "rāma\tpleasing\n"
        )


def test_parser_requires_required_headers():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse(
            "headword\tgrammatical_category\n"
            "rāma\tnoun\n"
        )


def test_parser_rejects_unknown_header_in_strict_mode():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse(
            "headword\tdefinition\tunknown_field\n"
            "rāma\tpleasing\tvalue\n"
        )


def test_parser_rejects_empty_source():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse("")


def test_parser_rejects_none():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(TypeError):
        parser.parse(None)


def test_parser_skips_blank_lines():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "\n"
        "rāma\tpleasing\n"
        "\n"
    )

    entries = parser.parse(text)

    assert len(entries) == 1


def test_parser_rejects_missing_headword():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse(
            "headword\tdefinition\n"
            "\tpleasing\n"
        )


def test_parser_rejects_missing_definition():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse(
            "headword\tdefinition\n"
            "rāma\t\n"
        )


def test_parser_rejects_extra_columns():
    parser = DelimitedMonierWilliamsParser()

    with pytest.raises(ValueError):
        parser.parse(
            "headword\tdefinition\n"
            "rāma\tpleasing\textra\n"
        )


def test_parser_normalizes_header_case_and_whitespace():
    parser = DelimitedMonierWilliamsParser()

    text = (
        " HEADWORD \t DEFINITION \n"
        "rāma\tpleasing\n"
    )

    entries = parser.parse(text)

    assert entries[0].headword == "rāma"


def test_parser_iter_parse():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
        "hari\tbrown\n"
    )

    entries = list(parser.iter_parse(text))

    assert len(entries) == 2
    assert entries[0].headword == "rāma"
    assert entries[1].headword == "hari"

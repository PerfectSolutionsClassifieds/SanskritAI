
from pathlib import Path

from SanskritAI.acquisition.knowledge.parsers.monier_williams_parser import (
    MonierWilliamsParser,
)
from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


# ============================================================
# Construction
# ============================================================

def test_default_parser_metadata():
    parser = MonierWilliamsParser()

    assert parser.source_name == "Monier-Williams"
    assert parser.source_version == "unknown"
    assert parser.encoding == "utf-8"


# ============================================================
# Record Iteration
# ============================================================

def test_iter_records_skips_blank_lines(tmp_path):
    source = tmp_path / "mw.txt"

    source.write_text(
        "agni fire\n"
        "\n"
        "indra king\n"
        "   \n"
        "deva god\n",
        encoding="utf-8",
    )

    parser = MonierWilliamsParser()

    records = tuple(parser.iter_records(source))

    assert records == (
        "agni fire",
        "indra king",
        "deva god",
    )


def test_iter_records_strips_whitespace(tmp_path):
    source = tmp_path / "mw.txt"

    source.write_text(
        "  agni fire  \n"
        "  indra king\n",
        encoding="utf-8",
    )

    parser = MonierWilliamsParser()

    records = tuple(parser.iter_records(source))

    assert records == (
        "agni fire",
        "indra king",
    )


# ============================================================
# Headword Extraction
# ============================================================

def test_extract_headword_returns_first_token():
    parser = MonierWilliamsParser()

    assert parser.extract_headword("agni fire flame") == "agni"


def test_extract_headword_handles_single_token():
    parser = MonierWilliamsParser()

    assert parser.extract_headword("agni") == "agni"


# ============================================================
# Record Parsing
# ============================================================

def test_parse_record_creates_raw_lexical_entry():
    parser = MonierWilliamsParser()

    entry = parser.parse_record("agni fire flame")

    assert isinstance(entry, RawLexicalEntry)
    assert entry.source_name == "Monier-Williams"
    assert entry.source_version == "unknown"
    assert entry.source_record_id == "agni"
    assert entry.headword == "agni"
    assert entry.raw_text == "agni fire flame"


# ============================================================
# Complete Parse
# ============================================================

def test_parse_returns_tuple_of_raw_entries(tmp_path):
    source = tmp_path / "mw.txt"

    source.write_text(
        "agni fire\n"
        "indra king\n"
        "deva god\n",
        encoding="utf-8",
    )

    parser = MonierWilliamsParser()

    entries = parser.parse(source)

    assert isinstance(entries, tuple)
    assert len(entries) == 3

    assert entries[0].headword == "agni"
    assert entries[1].headword == "indra"
    assert entries[2].headword == "deva"


def test_parse_empty_source_returns_empty_tuple(tmp_path):
    source = tmp_path / "empty.txt"

    source.write_text("", encoding="utf-8")

    parser = MonierWilliamsParser()

    assert parser.parse(source) == ()


# ============================================================
# Summary
# ============================================================

def test_summary_contains_parser_metadata():
    parser = MonierWilliamsParser()

    summary = parser.summary()

    assert summary == {
        "parser": "MonierWilliamsParser",
        "source": "Monier-Williams",
        "version": "unknown",
        "encoding": "utf-8",
    }


# ============================================================
# String Representation
# ============================================================

def test_string_representation():
    parser = MonierWilliamsParser()

    assert str(parser) == (
        "MonierWilliamsParser(source='Monier-Williams')"
    )

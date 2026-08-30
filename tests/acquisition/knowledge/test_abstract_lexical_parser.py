
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from SanskritAI.acquisition.knowledge.abstract_lexical_parser import (
    AbstractLexicalParser,
)
from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


# ---------------------------------------------------------------------------
# Concrete parser used exclusively for testing
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class _ConcreteParser(AbstractLexicalParser):
    """
    Minimal concrete implementation of AbstractLexicalParser.

    The implementation deliberately performs only structural extraction:
    raw records are converted into RawLexicalEntry objects while preserving
    source provenance.
    """

    def parse(
        self,
        source: Path,
    ) -> tuple[RawLexicalEntry, ...]:
        return tuple(
            entry
            for record in self.iter_records(source)
            if (
                entry := self.parse_record(record)
            ) is not None
        )

    def iter_records(
        self,
        source: Path,
    ):
        with source.open(
            "r",
            encoding=self.encoding,
        ) as handle:
            yield from handle

    def parse_record(
        self,
        record: str,
    ) -> RawLexicalEntry | None:

        value = record.strip()

        if not value:
            return None

        return RawLexicalEntry(
            source_name=self.source_name,
            source_version=self.source_version,
            source_record_id=f"record-{value}",
            headword=value,
            raw_text=value,
        )


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_parser(
    *,
    source_name: str = "Test Dictionary",
    source_version: str = "unknown",
    encoding: str = "utf-8",
) -> _ConcreteParser:

    return _ConcreteParser(
        source_name=source_name,
        source_version=source_version,
        encoding=encoding,
    )


# ---------------------------------------------------------------------------
# Abstract contract
# ---------------------------------------------------------------------------

def test_parser_is_abstract():
    """
    AbstractLexicalParser cannot be instantiated directly because
    parse(), iter_records(), and parse_record() are abstract.
    """

    with pytest.raises(TypeError):
        AbstractLexicalParser(
            source_name="Test Dictionary",
        )


def test_concrete_parser_is_instantiable():
    parser = make_parser()

    assert isinstance(
        parser,
        AbstractLexicalParser,
    )


# ---------------------------------------------------------------------------
# Parser identity
# ---------------------------------------------------------------------------

def test_identifier_returns_concrete_class_name():
    parser = make_parser()

    assert parser.identifier == "_ConcreteParser"


def test_summary_contains_parser_information():
    parser = make_parser(
        source_name="Test Dictionary",
        source_version="1.2",
        encoding="utf-16",
    )

    summary = parser.summary()

    assert summary["parser"] == "_ConcreteParser"
    assert summary["source"] == "Test Dictionary"
    assert summary["version"] == "1.2"
    assert summary["encoding"] == "utf-16"


def test_string_representation_contains_source():
    parser = make_parser(
        source_name="Test Dictionary",
    )

    value = str(parser)

    assert "_ConcreteParser" in value
    assert "Test Dictionary" in value


# ---------------------------------------------------------------------------
# Record iteration
# ---------------------------------------------------------------------------

def test_iter_records_reads_source_records(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "हरि\n",
        encoding="utf-8",
    )

    parser = make_parser()

    records = tuple(
        parser.iter_records(source)
    )

    assert records == (
        "राम\n",
        "हरि\n",
    )


def test_iter_records_preserves_raw_record_content(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "  राम  \n"
        "हरि\t\n",
        encoding="utf-8",
    )

    parser = make_parser()

    records = tuple(
        parser.iter_records(source)
    )

    assert records[0] == "  राम  \n"
    assert records[1] == "हरि\t\n"


def test_iter_records_uses_parser_encoding(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\nहरि\n",
        encoding="utf-16",
    )

    parser = make_parser(
        encoding="utf-16",
    )

    records = tuple(
        parser.iter_records(source)
    )

    assert records == (
        "राम\n",
        "हरि\n",
    )


# ---------------------------------------------------------------------------
# Record parsing
# ---------------------------------------------------------------------------

def test_parse_record_creates_raw_lexical_entry():
    parser = make_parser()

    entry = parser.parse_record(
        "राम",
    )

    assert isinstance(
        entry,
        RawLexicalEntry,
    )

    assert entry.headword == "राम"
    assert entry.raw_text == "राम"


def test_parse_record_preserves_source_provenance():
    parser = make_parser(
        source_name="Test Dictionary",
        source_version="2.0",
    )

    entry = parser.parse_record(
        "राम",
    )

    assert entry is not None
    assert entry.source_name == "Test Dictionary"
    assert entry.source_version == "2.0"
    assert entry.source_record_id == "record-राम"


def test_parse_record_strips_record_for_headword():
    parser = make_parser()

    entry = parser.parse_record(
        "  राम  ",
    )

    assert entry is not None
    assert entry.headword == "राम"
    assert entry.raw_text == "राम"


def test_parse_record_ignores_blank_records():
    parser = make_parser()

    assert parser.parse_record("") is None
    assert parser.parse_record("   ") is None
    assert parser.parse_record("\n") is None
    assert parser.parse_record("\t") is None


# ---------------------------------------------------------------------------
# Complete parsing
# ---------------------------------------------------------------------------

def test_parse_returns_raw_lexical_entries(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "हरि\n",
        encoding="utf-8",
    )

    parser = make_parser()

    result = parser.parse(source)

    assert isinstance(
        result,
        tuple,
    )

    assert len(result) == 2

    assert all(
        isinstance(
            entry,
            RawLexicalEntry,
        )
        for entry in result
    )

    assert result[0].headword == "राम"
    assert result[1].headword == "हरि"


def test_parse_preserves_record_order(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "हरि\n"
        "गोविन्द\n",
        encoding="utf-8",
    )

    parser = make_parser()

    result = parser.parse(source)

    assert [
        entry.headword
        for entry in result
    ] == [
        "राम",
        "हरि",
        "गोविन्द",
    ]


def test_parse_skips_blank_records(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "\n"
        "   \n"
        "हरि\n",
        encoding="utf-8",
    )

    parser = make_parser()

    result = parser.parse(source)

    assert [
        entry.headword
        for entry in result
    ] == [
        "राम",
        "हरि",
    ]


def test_parse_preserves_provenance_for_every_entry(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "हरि\n",
        encoding="utf-8",
    )

    parser = make_parser(
        source_name="Test Dictionary",
        source_version="1.5",
    )

    result = parser.parse(source)

    assert [
        entry.source_name
        for entry in result
    ] == [
        "Test Dictionary",
        "Test Dictionary",
    ]

    assert [
        entry.source_version
        for entry in result
    ] == [
        "1.5",
        "1.5",
    ]


def test_parse_assigns_distinct_source_record_ids(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "हरि\n",
        encoding="utf-8",
    )

    parser = make_parser()

    result = parser.parse(source)

    ids = [
        entry.source_record_id
        for entry in result
    ]

    assert ids == [
        "record-राम",
        "record-हरि",
    ]

    assert len(ids) == len(set(ids))


# ---------------------------------------------------------------------------
# Parser / RawLexicalEntry boundary
# ---------------------------------------------------------------------------

def test_parser_does_not_normalize_source_word():
    parser = make_parser()

    entry = parser.parse_record(
        "रामः",
    )

    assert entry is not None
    assert entry.headword == "रामः"
    assert entry.raw_text == "रामः"


def test_parser_does_not_create_canonical_lexical_objects():
    parser = make_parser()

    entry = parser.parse_record(
        "राम",
    )

    assert isinstance(
        entry,
        RawLexicalEntry,
    )


def test_parser_output_is_immutable():
    parser = make_parser()

    entry = parser.parse_record(
        "राम",
    )

    assert entry is not None

    with pytest.raises(
        AttributeError,
    ):
        entry.headword = "हरि"


# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------

def test_parse_missing_source_raises_file_not_found(tmp_path):
    source = tmp_path / "missing.txt"

    parser = make_parser()

    with pytest.raises(
        FileNotFoundError,
    ):
        parser.parse(source)


def test_parse_empty_source_returns_empty_tuple(tmp_path):
    source = tmp_path / "empty.txt"

    source.write_text(
        "",
        encoding="utf-8",
    )

    parser = make_parser()

    result = parser.parse(source)

    assert result == ()


# ---------------------------------------------------------------------------
# Structural properties
# ---------------------------------------------------------------------------

def test_parser_is_slot_based():
    parser = make_parser()

    assert not hasattr(
        parser,
        "__dict__",
    )


def test_parser_has_expected_configuration():
    parser = make_parser(
        source_name="Dictionary",
        source_version="3.0",
        encoding="utf-8",
    )

    assert parser.source_name == "Dictionary"
    assert parser.source_version == "3.0"
    assert parser.encoding == "utf-8"


from pathlib import Path

import pytest

from SanskritAI.acquisition.knowledge.abstract_lexical_parser import (
    AbstractLexicalParser,
)
from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


# ---------------------------------------------------------------------------
# Test implementation
# ---------------------------------------------------------------------------


class TestParser(AbstractLexicalParser):
    """
    Minimal concrete parser used to exercise the abstract parser contract.
    """

    def parse(
        self,
        source: Path,
    ) -> tuple[RawLexicalEntry, ...]:
        return tuple(
            entry
            for entry in (
                self.parse_record(record)
                for record in self.iter_records(source)
            )
            if entry is not None
        )

    def iter_records(
        self,
        source: Path,
    ):
        yield from source.read_text(
            encoding=self.encoding,
        ).splitlines()

    def parse_record(
        self,
        record: str,
    ) -> RawLexicalEntry | None:
        if not record.strip():
            return None

        return RawLexicalEntry(
            headword=record.strip(),
        )


def make_parser(**overrides):
    values = {
        "source_name": "Test Dictionary",
    }

    values.update(overrides)

    return TestParser(**values)


# ---------------------------------------------------------------------------
# Abstract contract
# ---------------------------------------------------------------------------


def test_abstract_parser_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractLexicalParser(
            source_name="Test Dictionary",
        )


def test_concrete_parser_can_be_instantiated():
    parser = make_parser()

    assert isinstance(parser, AbstractLexicalParser)


# ---------------------------------------------------------------------------
# Constructor metadata
# ---------------------------------------------------------------------------


def test_source_name_is_preserved():
    parser = make_parser(
        source_name="Monier-Williams",
    )

    assert parser.source_name == "Monier-Williams"


def test_default_source_version_is_unknown():
    parser = make_parser()

    assert parser.source_version == "unknown"


def test_default_encoding_is_utf8():
    parser = make_parser()

    assert parser.encoding == "utf-8"


def test_custom_parser_metadata_is_preserved():
    parser = make_parser(
        source_version="1899",
        encoding="latin-1",
    )

    assert parser.source_version == "1899"
    assert parser.encoding == "latin-1"


# ---------------------------------------------------------------------------
# Identifier
# ---------------------------------------------------------------------------


def test_identifier_defaults_to_concrete_class_name():
    parser = make_parser()

    assert parser.identifier == "TestParser"


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def test_summary_contains_parser_diagnostics():
    parser = make_parser(
        source_name="Monier-Williams",
        source_version="1899",
        encoding="utf-8",
    )

    summary = parser.summary()

    assert summary == {
        "parser": "TestParser",
        "source": "Monier-Williams",
        "version": "1899",
        "encoding": "utf-8",
    }


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------


def test_string_representation_contains_class_and_source():
    parser = make_parser(
        source_name="Monier-Williams",
    )

    assert str(parser) == (
        "TestParser(source='Monier-Williams')"
    )


# ---------------------------------------------------------------------------
# Parsing contract
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

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(
        isinstance(entry, RawLexicalEntry)
        for entry in result
    )


def test_iter_records_returns_raw_records(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n"
        "हरि\n",
        encoding="utf-8",
    )

    parser = make_parser()

    result = list(parser.iter_records(source))

    assert result == [
        "राम",
        "हरि",
    ]


def test_parse_record_returns_none_for_empty_record():
    parser = make_parser()

    assert parser.parse_record("") is None
    assert parser.parse_record("   ") is None


def test_parse_record_creates_raw_lexical_entry():
    parser = make_parser()

    entry = parser.parse_record("राम")

    assert isinstance(entry, RawLexicalEntry)
    assert entry.headword == "राम"


# ---------------------------------------------------------------------------
# Encoding behavior
# ---------------------------------------------------------------------------


def test_parser_uses_declared_encoding(tmp_path):
    source = tmp_path / "dictionary.txt"

    source.write_text(
        "राम\n",
        encoding="utf-8",
    )

    parser = make_parser(
        encoding="utf-8",
    )

    records = list(parser.iter_records(source))

    assert records == ["राम"]


from pathlib import Path

from SanskritAI.acquisition.lexical.monier_williams import (
    DelimitedMonierWilliamsParser,
    FileMonierWilliamsSource,
    MonierWilliamsSource,
    MonierWilliamsSourceParser,
)


class StubSource(MonierWilliamsSource):

    def __init__(self, text: str):
        self.text = text

    def acquire(self) -> str:
        return self.text


def test_parser_accepts_extended_canonical_headers():
    parser = DelimitedMonierWilliamsParser()

    text = (
        "headword\ttransliteration\tdefinition\t"
        "grammatical_label\tsource_id\traw_text\n"
        "देव\tdeva\tgod\tm.\tmw-001\tदेव — god\n"
    )

    records = parser.parse(text)

    assert len(records) == 1
    assert records[0].headword == "देव"
    assert records[0].transliteration == "deva"
    assert records[0].definition == "god"
    assert records[0].grammatical_label == "m."
    assert records[0].source_id == "mw-001"
    assert records[0].raw_text == "देव — god"


def test_parser_empty_source_returns_empty_tuple():
    parser = DelimitedMonierWilliamsParser()

    assert parser.parse("") == ()


def test_parser_supports_custom_delimiter():
    parser = DelimitedMonierWilliamsParser(
        delimiter=",",
    )

    records = parser.parse(
        "headword,definition\n"
        "deva,god\n"
    )

    assert len(records) == 1
    assert records[0].headword == "deva"
    assert records[0].definition == "god"


def test_parser_supports_parse_lines():
    parser = DelimitedMonierWilliamsParser()

    records = parser.parse_lines(
        (
            "headword\tdefinition",
            "देव\tgod",
        )
    )

    assert len(records) == 1
    assert records[0].headword == "देव"


def test_file_source_exposes_source(tmp_path: Path):
    path = tmp_path / "mw.tsv"

    path.write_text(
        "headword\tdefinition\n"
        "deva\tgod\n",
        encoding="utf-8",
    )

    source = FileMonierWilliamsSource(path)

    assert source.source == "monier-williams"
    assert source.acquire().startswith("headword")


def test_lightweight_source_double_is_valid():
    source = StubSource(
        "headword\tdefinition\n"
        "देव\tgod\n"
    )

    assert source.source == "monier-williams"
    assert source.acquire().startswith("headword")


def test_source_parser_accepts_injected_acquirer():
    source = StubSource(
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
    )

    parser = MonierWilliamsSourceParser(
        acquirer=source,
    )

    records = parser.parse()

    assert len(records) == 1
    assert records[0].headword == "rāma"
    assert records[0].definition == "pleasing"


def test_source_parser_accepts_custom_parser():
    source = StubSource(
        "headword,definition\n"
        "rāma,pleasing\n"
    )

    parser = MonierWilliamsSourceParser(
        acquirer=source,
        parser=DelimitedMonierWilliamsParser(
            delimiter=",",
        ),
    )

    records = parser.parse()

    assert len(records) == 1
    assert records[0].headword == "rāma"

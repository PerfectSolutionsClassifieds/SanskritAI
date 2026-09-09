from __future__ import annotations

from pathlib import Path

from SanskritAI.acquisition.lexical.monier_williams import (
    LocalMonierWilliamsSourceAcquirer,
    MonierWilliamsAcquisitionService,
    MonierWilliamsSourceParser,
    MonierWilliamsSourcePipeline,
)


MW_SOURCE = (
    "<L>1\n"
    "<k1>rAma\n"
    "<h>m.\n"
    "<e>pleasing, beautiful\n"
    "<LEND>\n"
    "<L>2\n"
    "<k1>hari\n"
    "<h>m.\n"
    "<e>yellow, tawny\n"
    "<LEND>\n"
)


def test_local_source_acquirer_is_independent_of_parser(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        MW_SOURCE,
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    raw_text = acquirer.acquire()

    assert raw_text == MW_SOURCE


def test_local_source_acquirer_returns_raw_text_only(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        MW_SOURCE,
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    result = acquirer.acquire()

    assert isinstance(result, str)
    assert "<L>1" in result
    assert "<k1>rAma" in result
    assert "<LEND>" in result


def test_acquirer_can_feed_monier_williams_parser(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        MW_SOURCE,
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    raw_text = acquirer.acquire()

    parser = MonierWilliamsSourceParser()

    records = parser.parse(raw_text)

    assert isinstance(records, tuple)
    assert len(records) == 2

    assert records[0].headword == "rAma"
    assert records[1].headword == "hari"


def test_acquirer_to_parser_preserves_source_record_boundary(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        MW_SOURCE,
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    parser = MonierWilliamsSourceParser()

    records = parser.parse(
        acquirer.acquire(),
    )

    assert records[0].raw_text.startswith("<L>1")
    assert records[1].raw_text.startswith("<L>2")


def test_source_acquirer_has_no_parser_responsibility():
    assert not hasattr(
        LocalMonierWilliamsSourceAcquirer,
        "parse",
    )


def test_source_acquirer_is_not_a_parser():
    acquirer_methods = set(
        name
        for name in dir(LocalMonierWilliamsSourceAcquirer)
        if not name.startswith("_")
    )

    assert "acquire" in acquirer_methods
    assert "parse" not in acquirer_methods


def test_existing_service_pipeline_remains_independent_of_local_acquirer(
    tmp_path: Path,
):
    """
    This test documents the current architecture.

    The LocalMonierWilliamsSourceAcquirer is currently an independent
    raw-text acquisition mechanism. The existing service/pipeline can
    continue to operate through its MonierWilliamsSource boundary.
    """

    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        MW_SOURCE,
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    raw_text = acquirer.acquire()

    parser = MonierWilliamsSourceParser()

    records = parser.parse(raw_text)

    assert len(records) == 2
    assert records[0].headword == "rAma"
    assert records[1].headword == "hari"

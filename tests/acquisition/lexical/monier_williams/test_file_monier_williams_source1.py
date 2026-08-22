from __future__ import annotations

from pathlib import Path

from SanskritAI.acquisition.lexical.monier_williams import (
    FileMonierWilliamsSource,
)


def test_file_source_reads_utf8_content(
    tmp_path: Path,
):
    path = tmp_path / "mw.tsv"

    path.write_text(
        "headword\tdefinition\n"
        "deva\tgod\n",
        encoding="utf-8",
    )

    source = FileMonierWilliamsSource(path)

    assert source.source == "monier-williams"
    assert source.read() == (
        "headword\tdefinition\n"
        "deva\tgod\n"
    )


def test_file_source_accepts_string_path(
    tmp_path: Path,
):
    path = tmp_path / "mw.txt"

    path.write_text(
        "test",
        encoding="utf-8",
    )

    source = FileMonierWilliamsSource(
        str(path),
    )

    assert source.read() == "test"

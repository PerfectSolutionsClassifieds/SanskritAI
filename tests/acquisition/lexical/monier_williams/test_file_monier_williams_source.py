
from pathlib import Path

import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    FileMonierWilliamsSource,
)


def test_file_source_reads_text(tmp_path: Path):
    source_file = tmp_path / "mw.txt"

    source_file.write_text(
        "<L>1\n"
        "<k1>rAma\n"
        "<e>pleasing\n"
        "<LEND>\n",
        encoding="utf-8",
    )

    source = FileMonierWilliamsSource(source_file)

    assert source.read().startswith("<L>1")
    assert source.exists() is True


def test_file_source_identifier():
    source = FileMonierWilliamsSource("mw.txt")

    assert source.identifier == "monier-williams:file"


def test_file_source_name():
    source = FileMonierWilliamsSource("mw.txt")

    assert "Monier-Williams" in source.source_name


def test_file_source_exposes_path():
    source = FileMonierWilliamsSource("mw.txt")

    assert source.path == Path("mw.txt")


def test_file_source_missing_file(tmp_path):
    source = FileMonierWilliamsSource(
        tmp_path / "missing.txt"
    )

    assert source.exists() is False

    with pytest.raises(FileNotFoundError):
        source.read()


def test_file_source_rejects_directory(tmp_path):
    source = FileMonierWilliamsSource(tmp_path)

    with pytest.raises(ValueError):
        source.read()


from pathlib import Path

import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    LocalMonierWilliamsSourceAcquirer,
)


def test_local_acquirer_reads_source(tmp_path: Path):
    source = tmp_path / "mw.tsv"

    source.write_text(
        "headword\tdefinition\n"
        "rāma\tpleasing\n",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(source)

    assert acquirer.acquire() == (
        "headword\tdefinition\n"
        "rāma\tpleasing\n"
    )


def test_local_acquirer_exposes_path(tmp_path):
    source = tmp_path / "mw.tsv"

    acquirer = LocalMonierWilliamsSourceAcquirer(source)

    assert acquirer.path == source


def test_local_acquirer_rejects_missing_file(tmp_path):
    source = tmp_path / "missing.tsv"

    acquirer = LocalMonierWilliamsSourceAcquirer(source)

    with pytest.raises(FileNotFoundError):
        acquirer.acquire()


def test_local_acquirer_rejects_directory(tmp_path):
    acquirer = LocalMonierWilliamsSourceAcquirer(tmp_path)

    with pytest.raises(ValueError):
        acquirer.acquire()

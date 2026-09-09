
from __future__ import annotations

from pathlib import Path

import pytest

from SanskritAI.acquisition.lexical.monier_williams.local_monier_williams_source_acquirer import (
    LocalMonierWilliamsSourceAcquirer,
)
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source import (
    MonierWilliamsSource,
)


class ReadOnlySource(MonierWilliamsSource):
    """Modern source implementation using read()."""

    def __init__(self, text: str) -> None:
        self._text = text

    def read(self) -> str:
        return self._text


class AcquireOnlySource:
    """
    Legacy/lightweight source implementation exposing acquire()
    without requiring read().
    """

    SOURCE = "monier-williams"

    @property
    def source(self) -> str:
        return self.SOURCE

    @property
    def identifier(self) -> str:
        return self.SOURCE

    @property
    def source_name(self) -> str:
        return "Monier-Williams"

    def acquire(self) -> str:
        return "acquired source text"


class InvalidSource:
    """Invalid source exposing neither read() nor acquire()."""

    pass


def test_read_based_source_is_supported() -> None:
    source = ReadOnlySource("raw source text")

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    result = service.acquire()

    assert result.text == "raw source text"
    assert result.source_identifier == "monier-williams"
    assert result.source_name == "Monier-Williams"


def test_source_read_returns_raw_content_unchanged() -> None:
    source = ReadOnlySource(
        "  raw\nsource\ntext  ",
    )

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    assert service.read() == "  raw\nsource\ntext  "


def test_acquire_only_compatibility_source_is_supported() -> None:
    source = AcquireOnlySource()

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    result = service.acquire()

    assert result.text == "acquired source text"
    assert result.source_identifier == "monier-williams"
    assert result.source_name == "Monier-Williams"


def test_acquire_only_source_is_supported_by_read_boundary() -> None:
    source = AcquireOnlySource()

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    assert service.read() == "acquired source text"


def test_invalid_source_fails_with_explicit_contract_error() -> None:
    source = InvalidSource()

    service = MonierWilliamsAcquisitionService(
        source=source,  # type: ignore[arg-type]
    )

    with pytest.raises(
        TypeError,
        match="must provide either read\\(\\) or acquire\\(\\)",
    ):
        service.read()


def test_local_source_acquirer_reads_text(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "mw.txt"

    source_file.write_text(
        "Monier-Williams source",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    assert acquirer.acquire() == "Monier-Williams source"


def test_local_source_acquirer_exposes_path(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "mw.txt"

    source_file.write_text(
        "source",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    assert acquirer.path == source_file


def test_local_source_acquirer_exposes_encoding(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "mw.txt"

    source_file.write_text(
        "source",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
        encoding="utf-8",
    )

    assert acquirer.encoding == "utf-8"


def test_local_source_acquirer_rejects_missing_file(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "missing.txt"

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_file,
    )

    with pytest.raises(FileNotFoundError):
        acquirer.acquire()


def test_local_source_acquirer_rejects_directory(
    tmp_path: Path,
) -> None:
    source_directory = tmp_path / "directory"
    source_directory.mkdir()

    acquirer = LocalMonierWilliamsSourceAcquirer(
        source_directory,
    )

    with pytest.raises(ValueError):
        acquirer.acquire()


from __future__ import annotations

from pathlib import Path

from .monier_williams_source_acquirer import (
    MonierWilliamsSourceAcquirer,
)


class LocalMonierWilliamsSourceAcquirer(
    MonierWilliamsSourceAcquirer
):
    """
    Acquires Monier–Williams source data from a local file.

    This implementation intentionally performs no parsing. Its sole
    responsibility is source acquisition and text decoding.
    """

    DEFAULT_ENCODING = "utf-8"

    def __init__(
        self,
        path: str | Path,
        *,
        encoding: str = DEFAULT_ENCODING,
    ) -> None:
        self._path = Path(path)
        self._encoding = encoding

    @property
    def path(self) -> Path:
        return self._path

    @property
    def encoding(self) -> str:
        return self._encoding

    def acquire(self) -> str:
        if not self._path.exists():
            raise FileNotFoundError(
                f"Monier-Williams source does not exist: {self._path}"
            )

        if not self._path.is_file():
            raise ValueError(
                f"Monier-Williams source is not a file: {self._path}"
            )

        return self._path.read_text(
            encoding=self._encoding,
        )

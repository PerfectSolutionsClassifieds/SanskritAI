
from __future__ import annotations

from pathlib import Path

from .monier_williams_source import MonierWilliamsSource


class FileMonierWilliamsSource(MonierWilliamsSource):
    """
    Monier-Williams source backed by a local UTF-8 file.
    """

    source = "monier-williams"

    def __init__(
        self,
        path: str | Path,
        *,
        encoding: str = "utf-8",
    ) -> None:
        self.path = Path(path)
        self.encoding = encoding

    def acquire(self) -> str:
        if not self.path.exists():
            raise FileNotFoundError(self.path)

        if not self.path.is_file():
            raise ValueError(
                f"Monier-Williams source is not a file: {self.path}"
            )

        return self.path.read_text(
            encoding=self.encoding,
        )

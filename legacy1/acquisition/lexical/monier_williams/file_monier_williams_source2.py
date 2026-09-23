
from __future__ import annotations

"""
SanskritAI
==========

File-backed Monier-Williams Source
----------------------------------
"""

from pathlib import Path

from .monier_williams_source import MonierWilliamsSource


class FileMonierWilliamsSource(MonierWilliamsSource):
    """
    Read a Monier-Williams source from a UTF-8 text file.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    @property
    def source(self) -> str:
        return "monier-williams"

    @property
    def source_name(self) -> str:
        return "Monier-Williams"

    @property
    def identifier(self) -> str:
        return "monier-williams:file"

    def exists(self) -> bool:
        return self.path.is_file()

    def acquire(self) -> str:
        if self.path.is_dir():
            raise ValueError(
                f"Monier-Williams source path is a directory: {self.path}"
            )

        if not self.path.exists():
            raise FileNotFoundError(
                f"Monier-Williams source file does not exist: {self.path}"
            )

        if not self.path.is_file():
            raise ValueError(
                f"Monier-Williams source path is not a file: {self.path}"
            )

        return self.path.read_text(encoding="utf-8")

    def read(self) -> str:
        return self.acquire()

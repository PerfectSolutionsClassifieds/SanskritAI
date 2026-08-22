from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .monier_williams_source import MonierWilliamsSource


@dataclass(frozen=True, slots=True)
class FileMonierWilliamsSource(MonierWilliamsSource):
    """Read a locally acquired Monier-Williams source file."""

    path: Path | str
    encoding: str = "utf-8"

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", Path(self.path))

        if not isinstance(self.encoding, str):
            raise TypeError("encoding must be a string")

    @property
    def identifier(self) -> str:
        return "monier-williams:file"

    @property
    def source_name(self) -> str:
        return "Monier-Williams"

    def exists(self) -> bool:
        return self.path.is_file()

    def read(self) -> str:
        if self.path.exists() and self.path.is_dir():
            raise ValueError(
                f"Monier-Williams source path is a directory: {self.path}"
            )

        return self.path.read_text(encoding=self.encoding)

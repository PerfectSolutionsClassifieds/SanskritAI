from __future__ import annotations

"""
SanskritAI
==========

File-based Monier-Williams Source
---------------------------------

Reads a locally acquired Monier-Williams source file.

The implementation intentionally performs no parsing.

This allows:

    acquisition != parsing

and permits future source implementations such as:

* HTTP source
* archive source
* SQLite source
* JSON source
* XML source
* compressed source
"""

from dataclasses import dataclass
from pathlib import Path

from .monier_williams_source import MonierWilliamsSource


@dataclass(frozen=True, slots=True)
class FileMonierWilliamsSource(MonierWilliamsSource):
    """
    Read Monier-Williams source content from a local file.
    """

    path: Path | str
    encoding: str = "utf-8"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "path",
            Path(self.path),
        )

        if not isinstance(self.encoding, str):
            raise TypeError("encoding must be a string")

    def read(self) -> str:
        """
        Read the source file completely.
        """
        return self.path.read_text(
            encoding=self.encoding,
        )

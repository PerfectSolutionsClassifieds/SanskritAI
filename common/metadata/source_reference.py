from __future__ import annotations

"""
SanskritAI
==========

Source Reference

Describes the origin of an acquired resource.

Version
-------
v0.1.0
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourceReference:
    """
    Reference to the origin of a corpus resource.
    """

    provider: str

    repository: str

    location: str

    local_path: Path | None = None

    def is_remote(self) -> bool:

        return self.location.startswith(
            ("http://", "https://")
        )

    def is_local(self) -> bool:

        return self.local_path is not None

    def to_dict(self) -> dict:

        return {

            "provider": self.provider,

            "repository": self.repository,

            "location": self.location,

            "local_path": (
                str(self.local_path)
                if self.local_path
                else None
            ),

        }

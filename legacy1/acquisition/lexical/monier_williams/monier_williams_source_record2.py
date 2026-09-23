
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Record
-----------------------------

Immutable acquisition-stage representation of one raw Monier-Williams
source record.

This object deliberately preserves the source representation.

It is NOT a canonical lexical/domain object.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class MonierWilliamsSourceRecord:
    """
    One source-level Monier-Williams record.

    Parameters
    ----------
    sequence:
        Positive source-record sequence number.

    raw_text:
        Complete raw source representation of the record.

    fields:
        Parsed source fields. Unknown fields are intentionally preserved.
    """

    sequence: int
    raw_text: str
    fields: Mapping[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.sequence, int):
            raise TypeError("sequence must be an integer")

        if self.sequence <= 0:
            raise ValueError("sequence must be positive")

        if not isinstance(self.raw_text, str):
            raise TypeError("raw_text must be a string")

        if not self.raw_text.strip():
            raise ValueError("raw_text must not be empty")

        if not isinstance(self.fields, Mapping):
            raise TypeError("fields must be a mapping")

        normalized = {
            str(key): "" if value is None else str(value)
            for key, value in self.fields.items()
        }

        object.__setattr__(
            self,
            "fields",
            MappingProxyType(normalized),
        )

    def get(self, name: str, default: str = "") -> str:
        """Return a source field without exposing mutable state."""
        return self.fields.get(name, default)

    @property
    def headword(self) -> str:
        return self.get("k1") or self.get("headword")

    @property
    def transliteration(self) -> str:
        return self.get("k1") or self.get("transliteration")

    @property
    def definition(self) -> str:
        return self.get("e") or self.get("definition")

    @property
    def grammatical_category(self) -> str:
        return (
            self.get("grammatical_category")
            or self.get("grammatical_label")
        )

    @property
    def grammatical_label(self) -> str:
        return self.grammatical_category

    @property
    def source_reference(self) -> str:
        return (
            self.get("source_reference")
            or self.get("source_id")
        )

    @property
    def source_id(self) -> str:
        return self.source_reference

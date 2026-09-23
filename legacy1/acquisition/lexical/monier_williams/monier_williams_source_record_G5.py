
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Record
-----------------------------

Immutable acquisition-stage representation of a single
Monier-Williams source record.

This object belongs strictly to the acquisition boundary.

It preserves source fields without converting them into
domain-level DictionaryEntry / DictionarySense objects.

The parser may expose convenient read-only properties, but
dynamic attributes are never assigned to the instance. This
keeps the object compatible with frozen/slotted dataclasses
and avoids collisions with read-only properties.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True, init=False)
class MonierWilliamsSourceRecord:
    """
    Raw acquisition-stage Monier-Williams record.

    Parameters
    ----------
    sequence:
        One-based source record sequence number.

    raw_text:
        Original source representation when explicitly supplied
        by the parser.

    fields:
        Normalized source fields.
    """

    sequence: int
    raw_text: str
    fields: Mapping[str, str]

    def __init__(
        self,
        sequence: int,
        raw_text: str,
        fields: Mapping[str, str],
        **kwargs: object,
    ) -> None:
        if sequence <= 0:
            raise ValueError("sequence must be positive")

        if not isinstance(raw_text, str):
            raise TypeError("raw_text must be a string")

        if not isinstance(fields, Mapping):
            raise TypeError("fields must be a mapping")

        normalized = {
            str(key).strip(): (
                "" if value is None else str(value).strip()
            )
            for key, value in fields.items()
        }

        # Optional compatibility values may be supplied by
        # older acquisition callers. They are stored only when
        # they do not collide with declared dataclass fields.
        for key, value in kwargs.items():
            normalized.setdefault(
                str(key).strip(),
                "" if value is None else str(value).strip(),
            )

        object.__setattr__(self, "sequence", sequence)
        object.__setattr__(self, "raw_text", raw_text)
        object.__setattr__(
            self,
            "fields",
            MappingProxyType(normalized),
        )

    @property
    def headword(self) -> str:
        return self.fields.get(
            "headword",
            self.fields.get("k1", ""),
        )

    @property
    def transliteration(self) -> str:
        return self.fields.get(
            "transliteration",
            "",
        )

    @property
    def definition(self) -> str:
        return self.fields.get(
            "definition",
            self.fields.get("e", ""),
        )

    @property
    def grammatical_label(self) -> str:
        return self.fields.get(
            "grammatical_label",
            "",
        )

    @property
    def grammatical_category(self) -> str:
        return self.fields.get(
            "grammatical_category",
            "",
        )

    @property
    def source(self) -> str:
        return self.fields.get(
            "source",
            "monier-williams",
        )

    @property
    def source_id(self) -> str:
        return self.fields.get(
            "source_id",
            "",
        )

    @property
    def source_reference(self) -> str:
        return self.fields.get(
            "source_reference",
            "",
        )

    @property
    def homonym(self) -> str:
        return self.fields.get(
            "homonym",
            self.fields.get("L", ""),
        )

    def get(
        self,
        key: str,
        default: str = "",
    ) -> str:
        """
        Return a normalized source field.
        """
        return self.fields.get(key, default)

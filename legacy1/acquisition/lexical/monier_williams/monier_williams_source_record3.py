from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True, init=False)
class MonierWilliamsSourceRecord:
    """
    Raw acquisition-stage Monier-Williams record.

    The record deliberately preserves source fields without converting
    them into canonical DictionaryEntry / DictionarySense objects.
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

        if not isinstance(raw_text, str) or not raw_text.strip():
            raise ValueError("raw_text must not be empty")

        if not isinstance(fields, Mapping):
            raise TypeError("fields must be a mapping")

        normalized = {
            str(key).strip(): "" if value is None else str(value).strip()
            for key, value in fields.items()
        }

        object.__setattr__(self, "sequence", sequence)
        object.__setattr__(self, "raw_text", raw_text)
        object.__setattr__(
            self,
            "fields",
            MappingProxyType(normalized),
        )

        # Compatibility aliases used by the source-format tests.
        for key, value in normalized.items():
            object.__setattr__(self, key, value)

        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    @property
    def headword(self) -> str:
        return self.fields.get("headword", self.fields.get("k1", ""))

    @property
    def transliteration(self) -> str:
        return self.fields.get("transliteration", self.fields.get("k1", ""))

    @property
    def definition(self) -> str:
        return self.fields.get("definition", self.fields.get("e", ""))

    @property
    def grammatical_label(self) -> str:
        return self.fields.get("grammatical_label", "")

    @property
    def grammatical_category(self) -> str:
        return self.fields.get("grammatical_category", "")

    @property
    def source_id(self) -> str:
        return self.fields.get("source_id", "")

    @property
    def homonym(self) -> str:
        return self.fields.get("homonym", self.fields.get("L", ""))

    def get(self, key: str, default: str = "") -> str:
        return self.fields.get(key, default)

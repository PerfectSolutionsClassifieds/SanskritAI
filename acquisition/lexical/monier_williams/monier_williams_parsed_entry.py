
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class MonierWilliamsParsedEntry:
    """
    Intermediate representation of a Monier–Williams source record.

    This is intentionally an acquisition-layer model. It must not expose
    DictionaryEntry or DictionarySense directly.
    """

    headword: str
    definition: str

    grammatical_category: str | None = None
    transliteration: str | None = None
    source_reference: str | None = None

    metadata: Mapping[str, str] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        if not self.headword.strip():
            raise ValueError("headword must not be empty")

        if not self.definition.strip():
            raise ValueError("definition must not be empty")

        object.__setattr__(
            self,
            "headword",
            self.headword.strip(),
        )

        object.__setattr__(
            self,
            "definition",
            self.definition.strip(),
        )

        if self.grammatical_category is not None:
            object.__setattr__(
                self,
                "grammatical_category",
                self.grammatical_category.strip(),
            )

        if self.transliteration is not None:
            object.__setattr__(
                self,
                "transliteration",
                self.transliteration.strip(),
            )

        if self.source_reference is not None:
            object.__setattr__(
                self,
                "source_reference",
                self.source_reference.strip(),
            )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MonierWilliamsSourceRecord:
    """
    One normalized record acquired from a Monier-Williams source.
    """

    headword: str
    definition: str

    transliteration: str = ""
    grammatical_label: str = ""
    source_id: str = ""
    raw_text: str = ""

    @property
    def source(self) -> str:
        return "monier-williams"

    @property
    def lemma(self) -> str:
        return self.headword

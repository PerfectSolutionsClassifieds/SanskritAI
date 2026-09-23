from __future__ import annotations

"""
Canonical parsed Amarakośa Synset.

Produced by parsers.

Consumed by builders.
"""

from dataclasses import dataclass, field


@dataclass(slots=True,frozen=True)
class SynsetRecord:
    """
    Parsed Amarakośa Synset.
    """

    identifier: str

    varga_identifier: str

    synset_identifier: str

    verse_number: int

    pada_number: int

    lexemes: list[str] = field(default_factory=list)

    commentary: str = ""

    notes: str = ""

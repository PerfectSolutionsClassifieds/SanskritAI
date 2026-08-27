from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Adapter Record
------------------------------

Represents one normalized record obtained from the
Monier-Williams dictionary source.

This class belongs to the adapter boundary.

It is intentionally separate from DictionaryEntry and
DictionarySense so that external dictionary-specific
structures do not leak into the lexical domain.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MonierWilliamsRecord:
    """
    Normalized Monier-Williams lexical record.

    Attributes
    ----------
    headword:
        Canonical dictionary headword.

    transliteration:
        IAST or source-provided transliteration.

    definition:
        Primary dictionary definition.

    grammatical_label:
        Optional grammatical/category information.

    source:
        Source identifier. Defaults to ``monier-williams``.

    source_id:
        Optional source-specific identifier.

    raw_text:
        Optional original source representation.
    """

    headword: str
    transliteration: str = ""
    definition: str = ""
    grammatical_label: str = ""
    source: str = "monier-williams"
    source_id: str = ""
    raw_text: str = ""

from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense Metadata

Metadata describing a single semantic sense within a
DictionaryEntry.

A DictionarySense represents one editorial meaning assigned
to a lexical entry by a specific dictionary.

Future versions may enrich a sense with examples,
citations, semantic domains, grammatical notes,
etymological information, and cross-references.

Version
-------
v0.3.0
"""

from dataclasses import dataclass, field

from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)


@dataclass(slots=True)
class DictionarySenseMetadata(BaseLexicalMetadata):
    """
    Metadata describing a dictionary sense.
    """

    # ---------------------------------------------------------
    # Editorial ordering
    # ---------------------------------------------------------

    sense_number: int = 1

    # ---------------------------------------------------------
    # Meaning
    # ---------------------------------------------------------

    definition: str = ""

    short_definition: str = ""

    gloss: str = ""

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    semantic_domain: str = ""

    usage_label: str = ""

    register: str = ""

    # ---------------------------------------------------------
    # Linguistic notes
    # ---------------------------------------------------------

    grammatical_note: str = ""

    etymology: str = ""

    # ---------------------------------------------------------
    # Supporting material
    # ---------------------------------------------------------

    examples: list[str] = field(default_factory=list)

    citations: list[str] = field(default_factory=list)

    cross_references: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Editorial notes
    # ---------------------------------------------------------

    notes: str = ""

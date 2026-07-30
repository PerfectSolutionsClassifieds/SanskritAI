from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Specification

Defines the declarative specification used to construct
canonical Sanskrit Pratyaya objects.

This module plays the same architectural role that
phoneme_specification.py plays for the Phonology Kernel and
dhatu_specification.py plays for the Dhatu Kernel.

The specification contains data only.
No construction logic belongs here.

Hierarchy
---------

PratyayaSpecification
        │
        ▼
PratyayaFactory
        │
        ▼
PratyayaCollection
        │
        ▼
PratyayaRepository

Future
------

Eventually the canonical Pratyaya inventory can be expanded
to cover:

    • Taddhita pratyayas

    • Kṛt pratyayas

    • Sup pratyayas

    • Tiṅ pratyayas

    • Primary and secondary affixes

Version
-------
v1.0.0
"""

from typing import NamedTuple


class PratyayaSpecification(
    NamedTuple
):
    """
    Declarative specification for constructing one Pratyaya.
    """

    identifier: str

    pratyaya: str

    transliteration: str

    meaning: str

    category: str

    notes: str = ""


# ---------------------------------------------------------
# Bootstrap Canonical Specification
# ---------------------------------------------------------

CANONICAL_PRATYAYA_SPECIFICATION: tuple[
    PratyayaSpecification,
    ...
] = (

    PratyayaSpecification(
        identifier="pratyaya.kta",
        pratyaya="क्त",
        transliteration="kta",
        meaning="past passive participle",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.ktva",
        pratyaya="क्त्वा",
        transliteration="ktvā",
        meaning="absolutive",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.tavya",
        pratyaya="तव्य",
        transliteration="tavya",
        meaning="to be done",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.tumun",
        pratyaya="तुमुन्",
        transliteration="tumun",
        meaning="infinitive",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.lyap",
        pratyaya="ल्यप्",
        transliteration="lyap",
        meaning="absolutive variant",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.shatr",
        pratyaya="शतृ",
        transliteration="śatṛ",
        meaning="present active participle",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.shanac",
        pratyaya="शानच्",
        transliteration="śānac",
        meaning="present middle participle",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.anIyA",
        pratyaya="अनीय",
        transliteration="anīya",
        meaning="desiderative / passive adjective",
        category="krit",
    ),

    PratyayaSpecification(
        identifier="pratyaya.nvul",
        pratyaya="ण्वुल्",
        transliteration="ṇvul",
        meaning="agentive",
        category="taddhita",
    ),

)

from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Operation

Defines the canonical operational behaviour performed by a
Paninian grammatical rule.

IMPORTANT
---------
This enumeration is intentionally orthogonal to
PaninianRuleCategory.

Category answers

    "What kind of sūtra is this?"

Examples

    Saṃjñā
    Vidhi
    Niyama
    Atideśa
    Adhikāra
    Paribhāṣā

Operation answers

    "What grammatical operation does it perform?"

Examples

    Lopa
    Āgama
    Ādeśa
    Sandhi
    Pratyaya
    Samāsa

This separation closely follows the architecture of the
Aṣṭādhyāyī while keeping SanskritAI extensible.

Examples
--------

1.1.1

Category

    SAMJNA

Operation

    NONE

----------------------------

6.1.77 iko yaṇ aci

Category

    VIDHI

Operation

    ADESHA

----------------------------

1.3.9 tasya lopaḥ

Category

    VIDHI

Operation

    LOPA

----------------------------

3.1.68 kartari śap

Category

    VIDHI

Operation

    PRATYAYA

Architecture
------------

PaninianRule
      │
      ├── Category
      │       └── PaninianRuleCategory
      │
      └── Operation
              └── PaninianRuleOperation

Future
------

The operation taxonomy is intentionally richer than the
initial implementation so that every future SanskritAI
kernel can classify its rules uniformly.

Version
-------
v1.0.0
"""

from enum import Enum
from enum import unique


@unique
class PaninianRuleOperation(str, Enum):
    """
    Canonical Paninian grammatical operations.
    """

    # ---------------------------------------------------------
    # No grammatical transformation
    # ---------------------------------------------------------

    NONE = "none"

    # ---------------------------------------------------------
    # Core derivational operations
    # ---------------------------------------------------------

    AGAMA = "agama"

    LOPA = "lopa"

    ADESHA = "adesha"

    # ---------------------------------------------------------
    # Phonological operations
    # ---------------------------------------------------------

    SANDHI = "sandhi"

    TRIPADI = "tripadi"

    GUNA = "guna"

    VRDDHI = "vrddhi"

    YAṆ = "yan"

    # ---------------------------------------------------------
    # Morphological operations
    # ---------------------------------------------------------

    PRATYAYA = "pratyaya"

    KRT = "krt"

    TADDHITA = "taddhita"

    STRI = "stri"

    SUP = "sup"

    TIN = "tin"

    VIKARANA = "vikarana"

    DHATU = "dhatu"

    ANGA = "anga"

    IT_SAMJNA = "it_samjna"

    # ---------------------------------------------------------
    # Compound formation
    # ---------------------------------------------------------

    SAMASA = "samasa"

    # ---------------------------------------------------------
    # Syntax
    # ---------------------------------------------------------

    VAKYA = "vakya"

    KARAKA = "karaka"

    VIBHAKTI = "vibhakti"

    # ---------------------------------------------------------
    # Semantics
    # ---------------------------------------------------------

    SEMANTIC = "semantic"

    ARTHA = "artha"

    # ---------------------------------------------------------
    # Prosody
    # ---------------------------------------------------------

    CHANDAS = "chandas"

    # ---------------------------------------------------------
    # Poetics
    # ---------------------------------------------------------

    ALANKARA = "alankara"

    # ---------------------------------------------------------
    # Knowledge Graph / AI
    # ---------------------------------------------------------

    KNOWLEDGE_GRAPH = "knowledge_graph"

    INFERENCE = "inference"

    ANNOTATION = "annotation"

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        """
        Human-readable operation name.
        """
        return self.value.replace("_", " ").title()

    def __str__(self) -> str:
        return self.value

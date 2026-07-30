from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Category

Defines the canonical grammatical categories of
Pāṇinian rules.

A Rule Category answers the question

    "What grammatical family does this rule belong to?"

This classification is independent of

    • execution priority
    • applicability
    • rule behaviour

Those concerns are modeled separately by

    • PaninianRuleType
    • PaninianRulePriority

The categories are intentionally broad so that every
sūtra of the Aṣṭādhyāyī can naturally belong to exactly
one primary category.

Version
-------
v1.0.0
"""

from enum import Enum
from enum import unique


@unique
class PaninianRuleCategory(str, Enum):
    """
    Canonical grammatical classification of Paninian rules.
    """

    # -----------------------------------------------------
    # Meta Grammar
    # -----------------------------------------------------

    SAMJNA = "samjna"
    PARIBHASHA = "paribhasha"
    ADHIKARA = "adhikara"

    # -----------------------------------------------------
    # Core Morphology
    # -----------------------------------------------------

    DHATU = "dhatu"
    PRATYAYA = "pratyaya"
    ANGA = "anga"

    # -----------------------------------------------------
    # Morphological Operations
    # -----------------------------------------------------

    AGAMA = "agama"
    LOPA = "lopa"
    ADESHA = "adesha"
    GUNA_VRDDHI = "guna_vrddhi"

    # -----------------------------------------------------
    # Phonology
    # -----------------------------------------------------

    SANDHI = "sandhi"
    TRIPADI = "tripadi"

    # -----------------------------------------------------
    # Semantic / Interpretive
    # -----------------------------------------------------

    KARAKA = "karaka"
    SAMASA = "samasa"
    TADDHITA = "taddhita"
    KRT = "krt"
    STRI = "stri"

    # -----------------------------------------------------
    # Miscellaneous
    # -----------------------------------------------------

    GENERAL = "general"

    # -----------------------------------------------------
    # Display
    # -----------------------------------------------------

    @property
    def display_name(self) -> str:
        """
        Human-readable category name.
        """

        return {
            self.SAMJNA: "Saṃjñā",
            self.PARIBHASHA: "Paribhāṣā",
            self.ADHIKARA: "Adhikāra",

            self.DHATU: "Dhātu",
            self.PRATYAYA: "Pratyaya",
            self.ANGA: "Aṅga",

            self.AGAMA: "Āgama",
            self.LOPA: "Lopa",
            self.ADESHA: "Ādeśa",
            self.GUNA_VRDDHI: "Guṇa–Vṛddhi",

            self.SANDHI: "Sandhi",
            self.TRIPADI: "Tripādī",

            self.KARAKA: "Kāraka",
            self.SAMASA: "Samāsa",
            self.TADDHITA: "Taddhita",
            self.KRT: "Kṛt",
            self.STRI: "Strī",

            self.GENERAL: "General",
        }[self]

    @property
    def is_meta_rule(self) -> bool:
        return self in {
            self.SAMJNA,
            self.PARIBHASHA,
            self.ADHIKARA,
        }

    @property
    def is_morphological(self) -> bool:
        return self in {
            self.DHATU,
            self.PRATYAYA,
            self.ANGA,
            self.AGAMA,
            self.LOPA,
            self.ADESHA,
            self.GUNA_VRDDHI,
        }

    @property
    def is_phonological(self) -> bool:
        return self in {
            self.SANDHI,
            self.TRIPADI,
        }

    @property
    def is_semantic(self) -> bool:
        return self in {
            self.KARAKA,
            self.SAMASA,
            self.TADDHITA,
            self.KRT,
            self.STRI,
        }

    def __str__(self) -> str:
        return self.display_name

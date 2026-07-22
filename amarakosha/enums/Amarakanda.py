from __future__ import annotations

"""
SanskritAI
==========

Amarakanda

Defines the three canonical kāṇḍas (books) of the
Amarakośa.

The Amarakośa is traditionally divided into three major
kāṇḍas:

1. Svargādikāṇḍa
2. Bhūvargakāṇḍa
3. Sāmānyādikāṇḍa

These form the highest level of the Amarakośa knowledge
hierarchy.

Version
-------
v0.4.0
"""

from enum import Enum


class Amarakanda(str, Enum):
    """
    Enumeration of the three canonical Amarakośa kāṇḍas.
    """

    SVARGADI = "svargadi"

    BHUVARGA = "bhuvarga"

    SAMANYADI = "samanyadi"

    # ---------------------------------------------------------
    # Display Names
    # ---------------------------------------------------------

    @property
    def english_name(self) -> str:
        """
        Human-readable English name.
        """
        return {
            Amarakanda.SVARGADI: "Svargādikāṇḍa",
            Amarakanda.BHUVARGA: "Bhūvargakāṇḍa",
            Amarakanda.SAMANYADI: "Sāmānyādikāṇḍa",
        }[self]

    # ---------------------------------------------------------

    @property
    def devanagari(self) -> str:
        """
        Traditional Devanāgarī representation.
        """
        return {
            Amarakanda.SVARGADI: "स्वर्गादिकाण्ड",
            Amarakanda.BHUVARGA: "भूवर्गकाण्ड",
            Amarakanda.SAMANYADI: "सामान्यादिकाण्ड",
        }[self]

    # ---------------------------------------------------------

    @property
    def iast(self) -> str:
        """
        IAST transliteration.
        """
        return {
            Amarakanda.SVARGADI: "Svargādikāṇḍa",
            Amarakanda.BHUVARGA: "Bhūvargakāṇḍa",
            Amarakanda.SAMANYADI: "Sāmānyādikāṇḍa",
        }[self]

    # ---------------------------------------------------------

    @property
    def order(self) -> int:
        """
        Canonical ordering within the Amarakośa.
        """
        return {
            Amarakanda.SVARGADI: 1,
            Amarakanda.BHUVARGA: 2,
            Amarakanda.SAMANYADI: 3,
        }[self]

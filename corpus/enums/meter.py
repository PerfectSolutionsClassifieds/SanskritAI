from __future__ import annotations

"""
SanskritAI
==========

Sanskrit Meter Enumeration

Canonical Sanskrit poetic metres.

Version
-------
v0.1.0
"""

from enum import Enum


class Meter(str, Enum):
    """
    Canonical Sanskrit metres.
    """

    UNKNOWN = "unknown"

    ANUSTUBH = "anustubh"

    GAYATRI = "gayatri"

    TRISTUBH = "tristubh"

    JAGATI = "jagati"

    PANKTI = "pankti"

    BRHATI = "brhati"

    USHNIH = "ushnih"

    ATIJAGATI = "atijagati"

    SATOBRHATI = "satobrhati"

    VIRAJ = "viraj"

    ARYA = "arya"

    VASANTATILAKA = "vasantatilaka"

    SARDULAVIKRIDITA = "sardulavikridita"

    #MANDĀKRĀNTĀ = "mandakranta"
    MANDAKRANTA = "mandakranta"

    MALINI = "malini"

    SIKHARINI = "sikharini"

    INDRAVAJRA = "indravajra"

    UPENDRAVAJRA = "upendravajra"

    # ---------------------------------------------------------

    @classmethod
    def from_string(
        cls,
        value: str | None,
    ) -> "Meter":
        """
        Parse safely from text.
        """

        if not value:
            return cls.UNKNOWN

        normalized = value.strip().lower()

        for item in cls:

            if item.value == normalized:
                return item

        return cls.UNKNOWN

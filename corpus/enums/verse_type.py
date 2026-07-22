from __future__ import annotations

"""
SanskritAI
==========

Verse Type Enumeration

Canonical textual unit classifications used throughout the
SanskritAI corpus model.

Version
-------
v0.1.0
"""

from enum import Enum


class VerseType(str, Enum):
    """
    Canonical verse classifications.
    """

    UNKNOWN = "unknown"

    SLOKA = "sloka"

    MANTRA = "mantra"

    RC = "rc"

    SUKTA = "sukta"

    SUTRA = "sutra"

    STANZA = "stanza"

    VERSE = "verse"

    PROSE = "prose"

    HYMN = "hymn"

    PRAYER = "prayer"

    COLLOPHON = "colophon"

    INVOCATION = "invocation"

    REFRAIN = "refrain"

    # ---------------------------------------------------------

    @classmethod
    def from_string(
        cls,
        value: str | None,
    ) -> "VerseType":
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

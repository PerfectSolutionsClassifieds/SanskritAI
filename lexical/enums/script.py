
from __future__ import annotations

"""
SanskritAI
==========

Lexical Script Enumeration
==========================

Defines the writing-system classification used by lexical records
and lexical domain builders.

Version
-------
v0.4.2
"""

from enum import Enum


class Script(
    str,
    Enum,
):
    """
    Writing system used to represent a lexical item.
    """

    DEVANAGARI = "devanagari"

    IAST = "iast"

    LATIN = "latin"

    UNKNOWN = "unknown"

    @classmethod
    def from_value(
        cls,
        value: str | "Script",
    ) -> "Script":
        """
        Convert a textual script representation into a Script member.
        """

        if isinstance(
            value,
            cls,
        ):
            return value

        normalized = value.strip().lower()

        if normalized in {
            "devanagari",
            "deva",
        }:
            return cls.DEVANAGARI

        if normalized in {
            "iast",
        }:
            return cls.IAST

        if normalized in {
            "latin",
        }:
            return cls.LATIN

        return cls.UNKNOWN

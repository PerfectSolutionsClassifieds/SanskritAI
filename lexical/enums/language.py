
from __future__ import annotations

"""
SanskritAI
==========

Lexical Language Enumeration
============================

Defines the language classification used by lexical records and
lexical domain builders.

Version
-------
v0.4.2
"""

from enum import Enum


class Language(
    str,
    Enum,
):
    """
    Language represented by a lexical resource or lexical record.
    """

    SANSKRIT = "sanskrit"

    UNKNOWN = "unknown"

    @classmethod
    def from_value(
        cls,
        value: str | "Language",
    ) -> "Language":
        """
        Convert a textual value into a Language member.

        The conversion is intentionally tolerant of common Sanskrit
        language representations used by acquisition pipelines.
        """

        if isinstance(
            value,
            cls,
        ):
            return value

        normalized = value.strip().lower()

        if normalized in {
            "sa",
            "san",
            "sanskrit",
        }:
            return cls.SANSKRIT

        return cls.UNKNOWN

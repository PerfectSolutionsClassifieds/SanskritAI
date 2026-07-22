from __future__ import annotations

"""
SanskritAI
==========

Paragraph Type Enumeration

Canonical paragraph classifications used throughout the corpus
model.

Version
-------
v0.1.0
"""

from enum import Enum


class ParagraphType(str, Enum):
    """
    Canonical paragraph classifications.
    """

    UNKNOWN = "unknown"

    DEFAULT = "default"

    VERSE_TEXT = "verse_text"

    PROSE = "prose"

    TRANSLATION = "translation"

    COMMENTARY = "commentary"

    FOOTNOTE = "footnote"

    APPARATUS = "apparatus"

    PREFACE = "preface"

    INTRODUCTION = "introduction"

    COLOPHON = "colophon"

    APPENDIX = "appendix"

    INDEX = "index"

    BIBLIOGRAPHY = "bibliography"

    # ---------------------------------------------------------

    @classmethod
    def from_string(
        cls,
        value: str | None,
    ) -> "ParagraphType":

        if not value:
            return cls.UNKNOWN

        normalized = value.strip().lower()

        for item in cls:

            if item.value == normalized:
                return item

        return cls.UNKNOWN

"""
SanskritAI
==========

Module:
    services.importers.line_classifier

Description
-----------
Classifies individual lines of Sanskrit corpus text into
high-level structural categories.

The classifier performs lightweight lexical analysis only.
It does not modify parser state or construct domain objects.

Typical workflow
----------------

Raw Line
    │
    ▼
LineClassifier
    │
    ▼
LineType
    │
    ▼
Parser State Machine

Version:
    v0.4.0
"""

from __future__ import annotations

import re
from enum import Enum


class LineType(Enum):
    """
    High-level line categories.
    """

    EMPTY = "Empty"

    COMMENT = "Comment"

    KANDA = "Kanda"

    VARGA = "Varga"

    VERSE = "Verse"

    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return self.value


class LineClassifier:
    """
    Generic line classifier.

    Notes
    -----
    Current implementation uses simple heuristics.

    Future versions may replace these rules with
    configurable regular expressions or grammar-based
    classification without changing the public API.
    """

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    COMMENT_PREFIXES = (
        "#",
        "//",
        ";",
        "%",
    )

    KANDA_PATTERN = re.compile(
        r"^\s*.*काण्ड.*$",
        re.IGNORECASE,
    )

    VARGA_PATTERN = re.compile(
        r"^\s*.*वर्ग.*$",
        re.IGNORECASE,
    )

    # Verse numbers:
    #
    # १
    # १२
    # 1
    # 25
    # १।
    # 12।
    #
    VERSE_PATTERN = re.compile(
        r"^\s*[\d०-९]+(?:[।.]*)?\s*$"
    )

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @classmethod
    def classify(
        cls,
        line: str,
    ) -> LineType:
        """
        Classify one input line.
        """

        text = line.strip()

        if not text:
            return LineType.EMPTY

        if text.startswith(cls.COMMENT_PREFIXES):
            return LineType.COMMENT

        if cls.KANDA_PATTERN.match(text):
            return LineType.KANDA

        if cls.VARGA_PATTERN.match(text):
            return LineType.VARGA

        if cls.VERSE_PATTERN.match(text):
            return LineType.VERSE

        return LineType.UNKNOWN

    # ---------------------------------------------------------
    # Convenience predicates
    # ---------------------------------------------------------

    @classmethod
    def is_structural(
        cls,
        line: str,
    ) -> bool:
        """
        True for structural elements.
        """

        return cls.classify(line) in (
            LineType.KANDA,
            LineType.VARGA,
            LineType.VERSE,
        )

    @classmethod
    def is_ignorable(
        cls,
        line: str,
    ) -> bool:
        """
        True if the parser may safely skip the line.
        """

        return cls.classify(line) in (
            LineType.EMPTY,
            LineType.COMMENT,
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return "LineClassifier()"

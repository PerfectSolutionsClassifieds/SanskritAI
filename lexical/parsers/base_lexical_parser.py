from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Parser

Abstract base class for all lexical parsers.

This class specializes the generic BaseParser for lexical
resources and provides common lexical parsing infrastructure.

Responsibilities
----------------
- Source normalization
- Lexical text normalization
- Script normalization hooks
- Common parser metadata

Concrete implementations
------------------------
- AmarakoshaLexicalParser
- MonierWilliamsParser
- ApteParser
- CustomDictionaryParser

Pipeline
--------

External Source
        ↓
BaseLexicalParser
        ↓
LexemeRecord

Version
-------
v0.6.0
"""

from abc import ABC
from typing import Iterable

from SanskritAI.core.parsers.base_parser import BaseParser
from SanskritAI.lexical.records.lexeme_record import LexemeRecord


class BaseLexicalParser(
    BaseParser[str],
    ABC,
):
    """
    Base class for all lexical parsers.
    """

    # ---------------------------------------------------------
    # Lexical normalization
    # ---------------------------------------------------------

    def normalize_text(
        self,
        text: str,
    ) -> str:
        """
        Normalize lexical text.

        Subclasses may override for source-specific behaviour.
        """
        return text.strip()

    def normalize_optional(
        self,
        text: str | None,
    ) -> str:
        """
        Normalize an optional text field.
        """
        if text is None:
            return ""
        return self.normalize_text(text)

    # ---------------------------------------------------------
    # Batch helpers
    # ---------------------------------------------------------

    def parse_lines(
        self,
        lines: Iterable[str],
    ) -> Iterable[LexemeRecord]:
        """
        Parse multiple textual lines into LexemeRecord objects.
        """
        for line in lines:
            line = self.normalize_text(line)

            if not line:
                continue

            yield self.parse(line)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def subsystem(self) -> str:
        """
        Parser subsystem name.
        """
        return "lexical"

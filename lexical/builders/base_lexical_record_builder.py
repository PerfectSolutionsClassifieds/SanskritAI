from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Record Builder

Abstract adapter responsible for converting immutable lexical
records into lexical domain objects.

This class specializes the generic RecordBuilder for the
Lexical subsystem and provides common extension points for all
lexical record builders.

Pipeline
--------

LexicalRecord
      ↓
LexicalValidator
      ↓
BaseLexicalRecordBuilder
      ↓
Lexical Domain Object

Concrete implementations
------------------------

LexemeRecordBuilder
DictionaryEntryRecordBuilder
DictionarySenseRecordBuilder
LexicalRelationRecordBuilder

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.builders.record_builder import RecordBuilder
from SanskritAI.core.typing import TObject
from SanskritAI.lexical.records.lexeme_record import LexemeRecord


class BaseLexicalRecordBuilder(
    RecordBuilder[str, TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for lexical record builders.

    Concrete subclasses adapt immutable lexical records into
    validated lexical domain objects.
    """

    @property
    def record_type(self) -> type[LexemeRecord]:
        """
        Returns the primary lexical record type supported by
        this builder.

        Concrete builders should override this property when
        supporting a more specific lexical record.
        """
        return LexemeRecord

    # ---------------------------------------------------------
    # Shared lexical mapping hooks
    # ---------------------------------------------------------

    def normalize_text(self, text: str) -> str:
        """
        Normalize lexical text before object construction.

        Subclasses may override to implement dictionary-specific
        normalization.
        """
        return text.strip()

    def normalize_optional(self, text: str | None) -> str:
        """
        Normalize an optional text field.
        """
        return "" if text is None else self.normalize_text(text)

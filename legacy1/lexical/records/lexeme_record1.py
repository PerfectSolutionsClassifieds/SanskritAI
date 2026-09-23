from __future__ import annotations

"""
SanskritAI
==========

Lexeme Record

Immutable parser record representing a single lexical unit.

LexemeRecord is the canonical parser output exchanged between
parsers, validators and record builders.

Pipeline
--------

Parser
    ↓
LexemeRecord
    ↓
LexemeValidator
    ↓
LexemeRecordBuilder
    ↓
Lexeme

Version
-------
v0.4.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.records.lexical_record import (
    LexicalRecord,
)
from SanskritAI.lexical.enums.language import Language
from SanskritAI.lexical.enums.script import Script
from SanskritAI.lexical.enums.dictionary_source import (
    DictionarySource,
)


@dataclass(slots=True, frozen=True)
class LexemeRecord(LexicalRecord[str]):
    """
    Immutable parser representation of a lexical item.
    """

    # ---------------------------------------------------------
    # Lexical identity
    # ---------------------------------------------------------

    lemma: str

    normalized: str = ""

    # ---------------------------------------------------------
    # Source information
    # ---------------------------------------------------------

    dictionary: DictionarySource = DictionarySource.UNKNOWN

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    language: Language = Language.SANSKRIT

    script: Script = Script.DEVANAGARI

    # ---------------------------------------------------------
    # Surface forms
    # ---------------------------------------------------------

    devanagari: str = ""

    iast: str = ""

    transliteration: str = ""

    # ---------------------------------------------------------
    # Semantic information
    # ---------------------------------------------------------

    gloss: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    tags: tuple[str, ...] = field(default_factory=tuple)

    notes: str = ""

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_text(self) -> str:
        """
        Preferred display representation.
        """
        return (
            self.devanagari
            or self.iast
            or self.lemma
        )

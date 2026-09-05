
from __future__ import annotations

"""
SanskritAI
==========

Lexeme Record
=============

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
v0.4.2
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.records.lexical_record import (
    LexicalRecord,
)

from SanskritAI.lexical.enums.language import (
    Language,
)

from SanskritAI.lexical.enums.script import (
    Script,
)

from SanskritAI.lexical.enums.dictionary_source import (
    DictionarySource,
)


@dataclass(
    slots=True,
    frozen=True,
    kw_only=True,
)
class LexemeRecord(
    LexicalRecord[str],
):
    """
    Immutable parser representation of a lexical item.

    ``kw_only=True`` is intentional.

    ``LexicalRecord`` contains inherited default-valued fields such
    as ``active``. Making the concrete lexical fields keyword-only
    prevents Python's dataclass field-ordering restriction from
    treating the required ``lemma`` field as a positional argument
    following an inherited default argument.

    The semantic contract remains unchanged:

        lemma
            required canonical lexical identity

        normalized
            normalized lexical form

        dictionary
            dictionary/source classification

        language / script
            lexical language and writing system

        surface forms
            Devanagari / IAST / transliteration

        gloss
            concise lexical meaning

        tags / notes
            extensibility and editorial information
    """

    # ---------------------------------------------------------
    # Lexical identity
    # ---------------------------------------------------------

    lemma: str

    normalized: str = ""

    # ---------------------------------------------------------
    # Source information
    # ---------------------------------------------------------

    dictionary: DictionarySource = (
        DictionarySource.UNKNOWN
    )

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

    tags: tuple[str, ...] = field(
        default_factory=tuple,
    )

    notes: str = ""

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_text(
        self,
    ) -> str:
        """
        Preferred human-readable representation.
        """

        return (
            self.devanagari
            or self.iast
            or self.lemma
        )

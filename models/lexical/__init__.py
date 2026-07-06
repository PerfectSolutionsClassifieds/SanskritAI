"""
SanskritAI
==========

Package:
    models.lexical

Description
-----------
Public API for the SanskritAI lexical domain model.

This package exposes the canonical lexical entities used
throughout the SanskritAI platform.

Version:
    v0.3.0 Final
"""

from .dictionary_sense import DictionarySense
from .dictionary_entry import DictionaryEntry
from .lexical_relation import LexicalRelation
from .lexeme import Lexeme

__all__ = (
    "DictionarySense",
    "DictionaryEntry",
    "LexicalRelation",
    "Lexeme",
)

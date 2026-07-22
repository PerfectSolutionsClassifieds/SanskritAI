"""
SanskritAI
==========

Amarakośa Integration
=====================

This package implements the Amarakośa knowledge model.

The Amarakośa is not treated merely as a dictionary but as a
canonical semantic knowledge base built around synonym groups
(synsets).

Architecture
------------

Corpus
    ↓
Lexical Layer
    ↓
Amarakośa Knowledge Layer

The lexical layer provides canonical lexical objects
(Lexeme, DictionaryEntry, DictionarySense,
LexicalRelation), while the Amarakośa layer organizes those
objects into traditional semantic structures.

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.enums.kanda import Amarakanda

__all__ = [
    "Amarakanda",
]

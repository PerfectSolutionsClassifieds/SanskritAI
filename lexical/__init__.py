"""
SanskritAI
==========

Lexical Layer

The lexical layer models words and lexical knowledge that
augment the Canonical Corpus Model.

The corpus hierarchy describes the physical organization of
texts (Document → Section → Verse → Paragraph → Line → Token),
while the lexical hierarchy describes linguistic entities
associated with those texts.

Typical hierarchy
-----------------

BaseLexicalNode
    ├── Lexeme
    ├── DictionaryEntry
    ├── DictionarySense
    └── LexicalRelation

Version
-------
v0.3.0
"""

from SanskritAI.lexical.models.base_lexical_node import BaseLexicalNode

__all__ = [
    "BaseLexicalNode",
]

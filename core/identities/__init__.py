"""
SanskritAI
==========

Identity Kernel

Provides immutable identifiers shared across all SanskritAI
subsystems.

The Identity Kernel establishes a common foundation for object
identity throughout the architecture.

Shared By
---------

- Records
- Corpus
- Lexical
- Amarakośa
- Builders
- Validators
- Parsers
- Tokenizers
- Diagnostics
- Serialization
- Future Morphological Engine

Architecture
------------

Identifier
      │
      ├── UUIDIdentifier
      ├── HierarchicalIdentifier
      ├── CorpusIdentifier
      ├── LexicalIdentifier
      └── KnowledgeIdentifier

Version
-------
v0.6.0
"""

from .identifier import Identifier
from .hierarchical_identifier import HierarchicalIdentifier
from .uuid_identifier import UUIDIdentifier
from .lexical_identifier import LexicalIdentifier
from .corpus_identifier import CorpusIdentifier
from .knowledge_identifier import KnowledgeIdentifier

__all__ = [
    "Identifier",
    "HierarchicalIdentifier",
    "UUIDIdentifier",
    "LexicalIdentifier",
    "CorpusIdentifier",
    "KnowledgeIdentifier",
]
